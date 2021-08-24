var thread_no = 0
var thread = {}

function mess_by_server(message_from_server) {
    $('.chatmess').append('<div class="mess_by_server p-2"><span class="left_text py-2 px-2">' + message_from_server + '</span></div>')
    $('.chatmess').scrollTop($('.chatmess')[0].scrollHeight);
}

function mess_by_client(message_from_client) {
    $('.chatmess').append('<div class="mess_by_client p-2"><span class="right_text py-2 px-2">' + message_from_client + '</span></div>')
    $('.chatmess').scrollTop($('.chatmess')[0].scrollHeight);
}

async function nlp(message_from_client) {
    let result;
    try {
        result = await $.ajax({
            type: 'POST',
            url: "/kubernetes/nlp",
            contentType: 'application/json',
            data: message_from_client,
        });
        return result;
    } catch (error) {
        console.error(error)
    }
}


async function k8s_ajax_request(sending_data, resource, action) {
    let result;
    try {

        result = await $.ajax({
            type: 'POST',
            url: "/kubernetes/" + resource + "/" + action,
            contentType: 'application/json',
            data: JSON.stringify(sending_data),
        });
        return result;
    } catch (error) {
        console.error(error)
    }
}

$(document).on('submit', '#kube-form', function(event) {
    event.preventDefault();
    // $("#chatbot-box").removeChild()
    // while($.contains( $("#chatbot-box").get(0), $(".config-form").get(0) )){
    //     $()
    // }
    message_from_client = $('#kube-form input').val().toLowerCase()
    mess_by_client(message_from_client)
    $(".config-form").closest("div").remove()
    $('#kube-form input').val('')
    $('#kube-form input').focus()
    $.ajax({
        type: 'POST',
        url: "/kubernetes/nlp",
        contentType: 'application/json',
        data: JSON.stringify(message_from_client),
        success: function(data) {
            if (data[0] === 0) {
                mess_by_server(resource_form(JSON.parse(data[1]), data[2], data[3]))
                $("#chatbot-box form").on('keypress', 'input', function(e) {
                    val = false
                    e.keyCode == 32 ? alert("Space key not supported") : val = true
                    return val
                })
            } else {
                mess_by_server(data[1])
            }
        }
    })
})


function resource_form(temp, product, action) {
    var formrow = ''
    for (var key in temp) {
        if (temp[key]["value"] === "null") {
            temp[key]["value"] = ""
        }
        formrow += `<div class="form-group"><div class="floating-label-group"><input class="form-control  rounded-0 input-sm" type="${temp[key]["dtype"]}" id="${key}" value="${temp[key]["value"]}" placeholder="${temp[key]["placeholder"]}" required autocomplete="off"/><label class="floating-label">${temp[key]["desc"]}</label></div></div>`
    }
    formrow += ` <div class="form-group"><button class="btn btn-outline-primary w-100" type="submit"><b>${action.toUpperCase().replace('_',' ')} ${product.toUpperCase()}</b></button></div>`
    form = `<form class='config-form' id="${action}-${product}"><div class='col'>${formrow}</div></form>`
    return form
}


$(document).on('submit', '.config-form', function(event) {
    event.preventDefault();
    $(".config-form").closest("div").remove()
    label_val = event.target.querySelectorAll('input')
    label = event.target.querySelectorAll('label')
    data = {}
    if (label.length != 0) {
        tempdiv = ''
        for (i = 0; i < label.length; i++) {
            tempdiv += `<div>${label[i].innerHTML} : ${$(label_val[i]).val()}</div>`
            data[`${label_val[i].id}`] = $(label_val[i]).val()
        }
        mess_by_client(tempdiv)
    }
    [action, resource] = event.target.id.split("-")
    k8s_ajax_request(data, resource, action).then(function(output) {
        mess_by_server(output[1])
        mess_by_server(`To see details <b class="show_detail_btn"data-toggle="modal" data-target="#modalPBottom" data-thread-no=${thread_no}>click</b>`)
        thread[thread_no] = output[2]
        thread_no += 1
    })
})

$(document).on('click', '.show_detail_btn', function(e) {
    $("#full_screen").attr("data-thread-no", e.target.getAttribute("data-thread-no"))
    $(".modal-p-bottom .modal-body .prettyprint").html(thread[e.target.getAttribute("data-thread-no")])
})


$(document).on('click', '#full_screen', function(e) {
    var page = window.open();
    page.document.open();
    page.document.write(`<html><pre class="prettyprint" style="border:0;">${thread[e.target.getAttribute("data-thread-no")]}</pre></html>`);
    page.document.close();
})