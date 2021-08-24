d_images = []
d_containers = []

// ajax request //

async function ajax_request(sending_data, resource, action) {
    let result;
    try {

        result = await $.ajax({
            type: 'POST',
            url: "/docker/" + resource + "/" + action,
            contentType: 'application/json',
            data: JSON.stringify(sending_data),
        });
        return result;
    } catch (error) {
        console.error(error)
    }
}


// disable enter key //
$("#docker form").on('keypress', 'input', function(e) {
    return !(e.keyCode == 32);
})

$(document).on('keypress', '.rename_form_popover_input', function(e) {
    return !(e.keyCode == 32);
})

$(document).on('keypress', '.commit_form_popover_input', function(e) {
    return !(e.keyCode == 32);
})

// popover //

var popOverSettings_rename = {
    sanitize: false,
    placement: 'right',
    container: 'body',
    html: true,
    content: function() {
        return $('.popover-content-rename').html();
    }

}
var popOverSettings_commit = {
    sanitize: false,
    placement: 'bottom',
    container: 'body',
    html: true,
    content: function() {
        return $('.popover-content-commit').html();
    }

}

// hide popover //

$('body').on('click', function(e) {
    $('[rel="popover_rename"]').each(function() {
        if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
            $(this).popover('hide');
        }
    });
    $('[rel="popover_commit"]').each(function() {
        if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
            $(this).popover('hide');
        }
    });
});

// close modal//

$('.modal-content').on("click", ".close_modal", function(event) {
    $('#staticBackdrop').modal('hide');
})


/*======================================================================================*/
//---------------------------------Container Operations----------------------------------//
/*======================================================================================*/


//-------------------------------------List Container-----------------------------------//

function container() {
    container_list = []
    ajax_request({}, "container", "list").then(function(output) {
        if (output[0] != 0) {
            $("#alertbox").append(alertfun("danger", "ERROR!!", "There is something wrong"))
            return false
        }
        output = output[1]
        $("#containers_catag tbody tr").remove();
        for (let i = 0; i < Object.keys(output).length; i++) {
            var newRow = $("<tr id=" + output[i]["ID"] + ">");
            var cols = '';
            container_list.push(output[i]["Names"])
            cols += '<th scope="row">' + (i + 1) + '</th>';
            cols += '<td ><i class="fa fa-edit rename" rel="popover_rename"> ' + output[i]["Names"] + '</td>';
            cols += '<td>' + output[i]["ID"] + '</td>';
            cols += '<td >' + output[i]["Image"] + '</td>';
            cols += '<td>' + output[i]["State"] + '</td>';
            cols += '<td>' + output[i]["Ports"] + '</td>';
            cols += '<td><button type="button" class="btn btn-outline-dark inspect "><i class="fa fa-search" ></button></td>';
            cols += '<td><button type="button" class="btn btn-outline-dark commit " rel="popover_commit"><i class="fa fa-clone" ></button></td>';
            if (output[i]["State"] != "running") {
                cols += '<td><button type="button" class="btn btn-outline-success play "><i class="fa fa-play" ></button></td>';
                cols += '<td><button type="button" class="btn btn-outline-danger trash_container"><i class="fa fa-trash" ></button></td>';
            } else {
                cols += '<td><button type="button" class="btn btn-outline-danger stop"><i class="fa fa-stop" ></i><span class="spinner-border spinner-border-sm d-none" role="status" aria-hidden="true"></span></button></td>';
                cols += '<td>Running</button></td>';
            }
            newRow.append(cols);
            $("#containers_catag tbody").append(newRow);
            $("[rel='popover_rename']").popover(popOverSettings_rename);
            $("[rel='popover_commit']").popover(popOverSettings_commit);


        }
        $("[rel='popover_rename']").on({
            "shown.bs.popover": function() {
                var input = $(".popover input.rename_form_popover_input");
                input.focus();
            }
        });
        $("[rel='popover_commit']").on({
            "shown.bs.popover": function() {
                var input = $(".popover input.commit_form_popover_input");
                input.focus();
            }
        });

        d_containers = container_list
    });
}

window.onload = container();


//-------------------------------------Add Container-----------------------------------//

$("#add_container").submit(function(event) {
    event.preventDefault();
    if (d_containers.indexOf($('#cn').val()) != -1) {
        $("#alertbox").append(alertfun("danger", "Container name not available!!", "Choose different container name"))
        return false
    }
    if (d_images.indexOf($('#in').val()) == -1) {
        $("#alertbox").append(alertfun("warning", "Image not exist!!", "You can pull the image"))
        return false
    }

    if ($('#hp').val().length != 0 && $('#cp').val().length == 0) {
        $("#alertbox").append(alertfun("danger", "Missing Container Port!!", "Please provide container port"))
        return false
    }
    var sending_data = {
        "--name": $('#cn').val(),
        "-p": $('#hp').val(),
        "c_p": $('#cp').val(),
        "image": $('#in').val(),
    }
    ajax_request(sending_data, "container", "create").then(function(output) {
        console.log(output)
        if (output[0] == 2) {
            $("#alertbox").append(alertfun("danger", "ERROR!!", "host port already alloted"))
            return false
        }
        if (output[0] != 0) {
            $("#alertbox").append(alertfun("danger", "ERROR!!", "There is somthing wrong "))
            return false
        }
        $("#alertbox").append(alertfun("success", "Success!!", "Container launched successfully"))
        container()
    })
});


//-----------------------------------Start Container----------------------------------//

$("#containers_catag").on("click", ".play", function(event) {
    sendingdata = { 'id': $(this).closest("tr").attr('id') };
    ajax_request(sendingdata, "container", "start").then(function(output) {
        if (output[0] == 2) {
            $("#alertbox").append(alertfun("danger", "Port Not Available!!", output[1] + " is used by other process"))

        }

        if (output[0] != 0) {
            $("#alertbox").append(alertfun("danger", "ERROR!!", output[1]))
            return false
        }
        $("#alertbox").append(alertfun("success", sendingdata['id'] + "!!", "successfully started"))
        image()
        container()
    });
});

//-----------------------------------Rename Container----------------------------------//

$(document).on('submit', '#rename_form_popover', function(event) {
    event.preventDefault();
    new_container_name = ""
    popover_parent = $('[aria-describedby="' + $(".popover").attr('id') + '"]')
    container_id = popover_parent.closest("tr").attr('id')
    input_name = $(document).find('.rename_form_popover_input').each(function(e) {
        new_container_name = $(this).val()
    })
    if (d_containers.indexOf(new_container_name) != -1) {
        $("#alertbox").append(alertfun("danger", "Container name not available!!", "Choose different container name"))
        return false
    }
    if (new_container_name != "") {
        sendingdata = {
            "id": container_id,
            "new_container_name": new_container_name
        }
        ajax_request(sendingdata, "container", "rename").then(function(output) {
            if (output[0] != 0) {
                $("#alertbox").append(alertfun("danger", "ERROR!!", "There is something wrong"))
                return false
            }
            container()
            $("#alertbox").append(alertfun("success", "Success!!", "Container " + container_id + " has been renamed to " + new_container_name))
        });
    }
    popover_parent.popover('hide');
});

//-----------------------------------Commit Container----------------------------------//

$(document).on('submit', '#commit_form_popover', function(event) {
    event.preventDefault();
    new_image_name = ""
    popover_parent = $('[aria-describedby="' + $(".popover").attr('id') + '"]')
    container_id = popover_parent.closest("tr").attr('id')
    input_image_name = $(document).find('.commit_form_popover_input').each(function(e) {
        new_image_name = $(this).val()
    })
    if (d_images.indexOf(new_image_name) != -1) {
        $("#alertbox").append(alertfun("danger", "Error!!", "Choose different image name or tag from existing image"))
        return false
    }
    if (new_image_name != "") {
        sendingdata = {
            "id": container_id,
            "new_image_name": new_image_name
        }
        ajax_request(sendingdata, "container", "commit").then(function(output) {
            if (output[0] != 0) {
                $("#alertbox").append(alertfun("danger", "ERROR!!", "There is something wrong"))
                return false
            }
            image()
            $("#alertbox").append(alertfun("success", "Success!!", "Container " + container_id + " has been commited to " + new_image_name))
        });
    }
    popover_parent.popover('hide');
});

//------------------------------------Stop Container-----------------------------------//


$("#containers_catag").on("click", ".stop", function(event) {
    $(this).attr("disabled", true)
    $(this).find('i').addClass("d-none")
    $(this).find('span').removeClass("d-none")
    sendingdata = { 'id': $(this).closest("tr").attr('id') };
    ajax_request(sendingdata, "container", "stop").then(function(output) {
        if (output[0] != 0) {
            $("#alertbox").append(alertfun("danger", "ERROR!!", "There is something wrong"))
            return false
        }
        $("#alertbox").append(alertfun("success", sendingdata['id'] + "!!", "successfully stopped"))
        image()
        container()
    });
});
//-----------------------------------Delete Container----------------------------------//

$("#containers_catag").on("click", ".trash_container", function(event) {
    sendingdata = { 'id': $(this).closest("tr").attr('id') };
    ajax_request(sendingdata, "container", "remove").then(function(output) {
        if (output[0] != 0) {
            $("#alertbox").append(alertfun("danger", "ERROR!!", "There is something wrong"))
            return false
        }
        $("#alertbox").append(alertfun("success", sendingdata['id'] + "!!", "successfully deleted"))
        image()
        container()
    });
});


//-----------------------------Inspect Container and Image-----------------------------//


$('#docker').on("click", ".inspect", function(event) {
    sendingdata = { 'id': $(this).closest("tr").attr('id') };
    $("#staticBackdropLabel").html(sendingdata['id'])
    ajax_request(sendingdata, "container", "inspect").then(function(output) {
        if (output[0] != 0) {
            $("#alertbox").append(alertfun("danger", "ERROR!!", "There is something wrong"))
            return false
        }
        $('#staticBackdrop .modal-body .prettyprint').html(output[1])
        $('#staticBackdrop').modal('show');
    });

})

/*======================================================================================*/
//-----------------------------------IMAGE operations-----------------------------------//
/*======================================================================================*/


//--------------------------------------List Image--------------------------------------//


function image() {
    var img_list = []
    ajax_request({}, "image", "list").then(function(output) {
        if (output[0] != 0) {
            $("#alertbox").append(alertfun("danger", "ERROR!!", "There is something wrong"))
            return false
        }
        output = output[1]
        $("#images_catag tbody tr").remove();
        for (let i = 0; i < Object.keys(output).length; i++) {
            img_list.push(output[i]["Repository"] + ":" + output[i]["Tag"])
            var newRow = $("<tr id=" + output[i]['Repository'] + ':' + output[i]['Tag'] + ">");
            var cols = '';
            cols += '<th scope="row">' + (i + 1) + '</th>';
            cols += '<td >' + output[i]["Repository"] + '</td>';
            cols += '<td>' + output[i]["Tag"] + '</td>';
            cols += '<td >' + output[i]["ID"] + '</td>';
            cols += '<td style="min-width: 250px;">' + output[i]["CreatedAt"] + '</td>';
            cols += '<td>' + output[i]["Size"] + '</td>';
            cols += '<td><button type="button" class="btn btn-outline-dark inspect "><i class="fa fa-search" ></button></td>';
            cols += '<td><button type="button" class="btn btn-outline-danger trash_image"><i class="fa fa-trash" ></button></td>';
            newRow.append(cols);
            $("#images_catag tbody").append(newRow);
        }
        d_images = img_list
        $('#imagename option').remove();
        for (img = 0; img < img_list.length; img++) {
            $('#imagename').append('<option value="' + img_list[img] + '">')
        }
    });
}

window.onload = image();

//--------------------------------------Pull Image--------------------------------------//

$("#pull_image").submit(function(event) {
    event.preventDefault();
    sendingdata = { "id": $('#ni').val() }
    if (d_images.indexOf(sendingdata["id"]) != -1) {
        $("#alertbox").append(alertfun("warning", "Already available!!", "No need to download"))
        return false;
    }
    $("#pull").attr("disabled", true)
    $("#pull").html('Downloading...')

    $("#pull").find('span').removeClass("d-none")
    ajax_request(sendingdata, "image", "pull").then(function(output) {
        $("#pull").attr("disabled", false)
        $("#pull").html('Pull')
        if (output[0] != 0) {
            $("#alertbox").append(alertfun("danger", "ERROR!!", "There is something wrong"))
            return false
        }
        $("#alertbox").append(alertfun("success", "Download Complete!!", "Your image has been downloaded"))
        image()
    })

});


//-------------------------------------Delete Image-------------------------------------//

$("#images_catag").on("click", ".trash_image", function(event) {
    sendingdata = { 'id': $(this).closest("tr").attr('id') };
    console.log(sendingdata['id'])
    ajax_request(sendingdata, "image", "remove").then(function(output) {
        if (output[0] != 0) {
            $("#alertbox").append(alertfun("danger", "ERROR!!", "The " + sendingdata['id'] + " is in used"))
            return false
        }
        $("#alertbox").append(alertfun("success", sendingdata['id'] + "!!", "successfully deleted"))
        image()
        container()
    });
});