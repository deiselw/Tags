$("#create-tag-name").on("keyup", tryEnableCreateTag);
$("#create-tag-form").on("submit", createTag);
$(".js-delete-tag").on("click", deleteTag);
$(".js-tag-name").on("focusout", updateTagName);
$(".js-tag-name").on("keydown", handleTagNameEnter);
$(".js-popup").on("visibility-change", toggleHoverClass);

function focusOnTagName() {
	$("#create-tag-name").focus();
}

function tryEnableCreateTag(e) {
	if (e.which == 13) {
		return;
	}
	$("#create-tag-submit").prop("disabled", !$(this).val().trim());
}

function createTag(e) {
	e.preventDefault();
	this.color.value = parseInt(this.color.value.replace("#", ""), 16);
	if (isCreateTagFormValid()) {
		$.ajax({
		type: "POST",
		cache: false,
		url: $(this).attr("action"),
		data: $(this).serialize(),
		success: function(data) {
			resetCreateTagForm();
			$("#tag-list").html(data);
			connectTagEvents();
		},
		statusCode: {
			400: function(errors) {
				showFormError(errors);
			},
			500: function() {
				resetCreateTagForm();
			}
		}
	});
	}
}

function isCreateTagFormValid() {
	return $("#create-tag-name").val().trim() != "";
}

function deleteTag(e) {
	e.preventDefault();
	$.ajax({
		type: "POST",
		cache: false,
		url: $(this).attr("data-url"),
		data: {"id": $(this).attr("data-tag")},
		success: function(data) {
			$("#tag-" + data.tag_id).remove();
		},
		statusCode: {
			409: function(data) {
				$("#tag-list").html(data);
			}
		}
	});
}

function updateTagName(e) {
	var editedTagName = $(this).val().trim();
	if (validateUpdateTag(this.defaultValue, editedTagName)) {
		submitUpdateTagName(this.id.match(/[0-9]+/)[0], editedTagName);
	}else {
		$(this).val(this.defaultValue);
	}
}

function validateUpdateTag(tagName, editedTagName) {
	return editedTagName && editedTagName != tagName;
}

function submitUpdateTagColor(tagId, newTagColor, prevColor) {
	newTagColor = parseInt(newTagColor.replace("#", ""), 16);
	$.ajax({
		type: "POST",
		cache: false,
		url: "/update-tag",
		data: {'id': tagId, 'color': newTagColor},
		success: function(data) {
			$("#tag-list").html(data);
			connectTagEvents();
		},
		error: function() {
  			$("#js-colorsel-" + tagId).css("background-color", prevColor);
  			rgbHexEl = document.getElementById("js-rgbhex-" + tagId);
  			rgbHexEl.value = prevColor;
  			rgbHexEl.defaultValue = prevColor;
		},
		statusCode: {
			400: function(errors) {
				showFormError(errors);
			},
			409: function(data) {
				$("#tag-list").html(data);
			}
		}
	});
}

function submitUpdateTagName(tagId, newTagName) {
	$.ajax({
		type: "POST",
		cache: false,
		url: "/update-tag",
		data: {'id': tagId, 'name': newTagName},
		success: function(data) {
			$("#tag-list").html(data);
			connectTagEvents();
		},
		error: function() {
			resetTagName(tagId);
		},
		statusCode: {
			400: function(errors) {
				showFormError(errors);
			},
			409: function(data) {
				$("#tag-list").html(data);
			}
		}
	});
}

function submitColor(tagId, color, prevColor) {
	if (tagId == "form") {
		return;
	}
	submitUpdateTagColor(tagId, color);
}

function handleTagNameEnter(e) {
	if (e.which == 13) {
		e.preventDefault();
		$(this).blur();
	}
}

function resetCreateTagForm() {
	document.getElementById("create-tag-form").reset();
	$("#create-tag-submit").prop("disabled", true);
}

function connectTagEvents() {
	$(".js-delete-tag").off();
	$(".js-tag-name").off();
	$(".js-coloropt").off();
	$(".js-rgbhex").off();
	$(".js-popupbtn").off();
	$(".js-popup").off();

	$(".js-delete-tag").on("click", deleteTag);
	$(".js-tag-name").on("focusout", updateTagName);
	$(".js-tag-name").on("keydown", handleTagNameEnter);
	$(".js-coloropt").on("click", selectColorOpt);
	$(".js-rgbhex").on("change", selectRgbHex);
	$(".js-popupbtn").on("click", toggleVisibility);
	$(".js-popup").on("visibility-change", toggleHoverClass);
}

function showFormError(error) {
	var jsonErrors = error.responseJSON;
	var firstKey = Object.keys(jsonErrors)[0];
	showTagErrorMessage(jsonErrors[firstKey][0].message);
}

var errorMessageTimeout;
function showTagErrorMessage(errorMessage) {
	var errorMsgEl = $("#create-tag-error-msg");
	errorMsgEl.text(errorMessage);
	errorMsgEl.css("visibility", "visible");
	clearTimeout(errorMessageTimeout);
	errorMessageTimeout = setTimeout(fadeOutTagErrorMessage, 5000);
}

function fadeOutTagErrorMessage() {
	$("#create-tag-error-msg").fadeTo(500, 0, function() {
	   $(this).css("visibility", "hidden");
	   $(this).css("opacity", 1);    
	});
}

function resetTagName(tagId) {
	var tagEl = $("#tag-name-" + tagId);
	tagEl.val(tagEl.defaultValue);
}

function toggleHoverClass() {
	var id = this.id.replace("js-colorpalette-", "");
	if (id == "form") {
		return;
	}
	$("#js-colorsel" + id).toggleClass("visible");
}

// begin Node
$("#open-create-node-form").on("click", function() {
	
});