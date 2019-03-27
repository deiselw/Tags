// drawer
$(".js-push").on("click", function() {
	$(".leftcol").toggleClass("leftcol_pushed");
	$(".main").toggleClass("main_pushed");
});

// search
$(".js-note-search").on("keyup", function() {
	if (!this.value.trim()) {
		$(".js-notebox").removeClass("not-displayed");
		$(this).next(".js-search-reset").addClass("hidden");
		return;
	}
	$(this).next(".js-search-reset").removeClass("hidden");
	var val = this.value.trim().replace(/\s+/g, "|");
	var re = new RegExp(val, "i");
	$(".js-notebox").each(function() {
		re.test($(this).find(".js-note-title").text())
			|| re.test($(this).find(".js-note-text").text()) ?
			$(this).removeClass("not-displayed") :
			$(this).addClass("not-displayed");
	});
});
$(".js-tag-search").on("keyup", function() {
	if (!this.value.trim()) {
		$(".js-tagbox").removeClass("not-displayed");
		return;
	}
	/*var words = this.value.trim().split(" ");
	var i;
	for (i = 0; i < words.length; i++) {
		$searched.each(function() {
			words[i].test($(this).find(".js-search-val").val()) ?
				$(this).removeClass("not-displayed") :
				$(this).addClass("not-displayed");
		});
	}*/
	var val = this.value.trim().replace(/\s+/g, "|");
	var re = new RegExp(val, "i");
	$(".js-tagbox").each(function() {
		re.test($(this).find(".js-tag-input").val()) ?
			$(this).removeClass("not-displayed") :
			$(this).addClass("not-displayed");
	});
});
$(".js-search-reset").on("click", function() {
	$(this).addClass("hidden").prev(".js-search-input").val("");
	$("." + $(this).attr("data-search")).removeClass("not-displayed");
});

// feedback messages
var tagsapp = {
	alert: function(msg) {
		var $alert = $(".alert");
		if ($alert.hasClass("alert_active")) {
			$alert.clearQueue().removeClass("alert_active");
		}
		$(".alert__text").text(msg);
		$alert
			.addClass("alert_active")
			.delay(5000)
			.queue(function() {
				$(this).removeClass('alert_active').dequeue();
			});
	}, 
	dialog: function(title, text, cancelText, actionText, cancelCallback, actionCallback) {
		$window = $(".js-dialog-window");
		$window.find(".js-dialog-title").text(title);
		$window.find(".js-dialog-text").text(text);
		$cancel = $($window.find(".js-dialog-cancel"));
		$cancel.text(cancelText);
		$action = $($window.find(".js-dialog-action"));
		$action.text(actionText);
		$dialog = $($window.parent(".js-dialog"));
		$dialog
			.unbind()
			.click(function(e) {
				if (e.target == this) {
					$dialog.addClass("hidden");
				}
			});
		$window
			.find(".js-dialog-btn")
			.unbind()
			.click(function() {
				$dialog.addClass("hidden");
			});
		$cancel.click(cancelCallback);
		$action.click(actionCallback);
		$dialog.removeClass("hidden");
	}, 
	noteform: function(link, title, text, cancelCallback, actionCallback) {
		$window = $(".js-noteform-window");
		$window.find(".js-noteform-link").val(link);
		$window.find(".js-noteform-title").val(title);
		$textarea = $($window.find(".js-noteform-text"));
		$textarea.css("height", 0);
		$textarea.val(text).css("height", $textarea.prop("scrollHeight"));
		$dialog = $($window.parent(".js-noteform"));
		$dialog
			.unbind()
			.click(function(e) {
				if (e.target == this) {
					$dialog.addClass("hidden");
				}
			});
		$window
			.find(".js-noteform-btn")
			.unbind()
			.click(function() {
				$dialog.addClass("hidden");
			});
		$($window.find(".js-noteform-cancel")).click(cancelCallback);
		$($window.find(".js-noteform-action")).click(actionCallback);
		$dialog.removeClass("hidden");
	}
}

// fab animation
$(".action").on("click", function() {
	$(this)
		.toggleClass("action_add")
		.toggleClass("action_submit");
});
/* ----- END GENERAL / BEGIN TAG ----- */

$(".js-taglist")
	.on("focusin", ".js-tag-input", function() {
		$(this).select();
		$menu = $($(this).next(".js-tag-menu"));
		$menu
			.find(".js-tag-edit")
			.addClass("not-displayed");
		$menu
			.find(".js-tag-cancel")
			.removeClass("not-displayed");
	})
	.on("focusout", ".js-tag-input", function(e) {
		$(this).prop("disabled", true);
		$menu = $($(this).next(".js-tag-menu"));
		$menu
			.find(".js-tag-cancel")
			.addClass("not-displayed");
		$menu
			.find(".js-tag-edit")
			.removeClass("not-displayed");
	})
	.on("keydown", ".js-tag-input", function(e) {
		if (e.which == 32) { //space
			e.preventDefault();
			return;
		}
		if (e.which == 27) { //esc
			$(this)
				.val(this.defaultValue)
				.blur();
			return;
		}
		if (e.which == 13) { //enter
			$(this).blur();
			return;
		}
	})
	.on("change", ".js-tag-input", function(e) {
		if ($(e.target).hasClass(".js-tag-reset")
				|| $.trim($(this).val()) == "") {
			$(this).val(this.defaultValue);
			return; 
		}
		var tag = this;
		$.ajax({
			type: "POST",
			url: $(this).attr("data-url"),
			data: {'tag_name': $(this).val()}, 
			success: function(data) {
				$(".js-taglist").html(data.template);
				$(".js-notetag" + data.tag_id).find(".js-notetag-name").text(data.tag_name);
				tagsapp.alert("Tag name updated");
			}, 
			error: function() {
				$(tag).val(tag.defaultValue);
			}, 
			statusCode: {
				400: function(errors) {
					tagsapp.alert(errors.responseJSON.name[0].message);
				}, 
				409: function(data) {
					$(".js-taglist").html(data);
				}
			}
		});
	})
	.on("paste", ".js-tag-input", function() {
		$(this).val($(this).val().replace(/\s/g, ""));
	})
	.on("click", ".js-tag-edit", function() {
		$(this)
			.parent(".js-tag-menu")
			.prev(".js-tag-input")
			.prop("disabled", false)
			.focus();
	});

// tag delete
$(".js-taglist").on("click", ".js-tag-del", function() {
	$tagDel = $(this);
	tagsapp.dialog(
		"Delete tag?", 
		"The notes connected with your tag will continue to exists normally, but the tag will be deleted from all these notes.", 
		"cancel", 
		"delete", 
		function() {}, 
		function() {
			var $tagbox = $($tagDel.closest(".js-tagbox"));
			$.ajax({
				type: "POST",
				url: $tagDel.attr("data-url"),
				success: function(data) {
					$tagbox.remove();
					$(".js-notetag" + data.tag_id).remove();
					tagsapp.alert("Tag deleted");
				},
				statusCode: {
					409: function(data) {
						$(".js-taglist").html(data);
					}
				}
			});
		}
	);
});

// tag color update
$(".js-taglist").on("click", ".js-tag-upd-color", function() {
	if ($(this).hasClass(".colors__color_selected")) {
		return;
	}
	var $this = $(this);
	$.ajax({
		type: "POST",
		url: $(this).attr("data-url"),
		success: function(data) {
			$(".js-tag-upd-color").removeClass("colors__color_selected");
			$this.addClass("colors__color_selected");
			$this.closest(".js-tag-menu").closest(".js-tag-input").css("color", data.tag_color);
			$(".js-notetag" + data.tag_id).css("color", data.tag_color);
		}
	});
});

// form toggle
$(".js-form-action").on("click", function() {
	var form = $("." + $(this).attr("data-form"));
	if (form.hasClass("float-form__fields_active")) {
		form.removeClass("float-form__fields_active");
		form.trigger("formSubmit");
		return;
	}
	form.addClass("float-form__fields_active");
	form.find(".float-form__input").focus();
});

// tag form color
$(".js-tagform-color").on("click", function() {
	if ($(this).hasClass("colors__color_selected")) {
		return;
	}
	$(".js-tagform-color").removeClass("colors__color_selected");
	$(this).addClass("colors__color_selected");
});

// tag create
$(".js-tagform").on("formSubmit", function() {
	var name = $.trim($(".js-tagform-name").val());
	if (name == "") {
		return;
	}
	$.ajax({
		type: "POST",
		url: $(this).attr("data-url"),
		data: {'name': name, 'color': $(this).find(".colors__color_selected").attr("data-color")}, 
		success: function(data) {
			$(".js-taglist").html(data);
			tagsapp.alert("Tag created");
		},  
		statusCode: {
			400: function(errors) {
				tagsapp.alert(errors.responseJSON.name[0].message);
			}, 
			409: function(data) {
				$(".js-taglist").html(data);
			}
		}
	}).always(function() {
		$(".js-tagform-name").val("");
		$(".js-tagform-color").removeClass(".colors__color_selected");
		$(".js-tagform-color-dft").addClass(".colors__color_selected");
	});
});

/* ----- END TAG / BEGIN NOTE ----- */

// note
$(".js-notelist")
	.on("click", ".js-notetag-remove", function() {
		$.ajax({
			type: "POST",
			url: $(this).attr("data-url"),
			success: function(data) {
				$(".js-notetag" + data.tag_id).remove();
				tagsapp.alert("Tag removed from note");
			},
			statusCode: {
				409: function(data) {
					$(".js-notelist").html(data);
				}
			}
		});
	})
	.on("click", ".js-note-del", function() {
		$noteDel = $(this);
		tagsapp.dialog(
			"Delete note?", 
			"This can't be undone.", 
			"cancel", 
			"delete", 
			function() {}, 
			function() {
				var $notebox = $($noteDel.closest(".js-notebox"));
				$.ajax({
					type: "POST",
					url: $noteDel.attr("data-url"),
					success: function(data) {
						$notebox.remove();
						tagsapp.alert("Note deleted");
					},
					statusCode: {
						409: function(data) {
							$(".js-notelist").html(data);
						}
					}
				});
			}
		);
	})
	.on("click", ".js-note-edit", function() {
		$note = $(this).parent().prev(".js-note");
		tagsapp.noteform(
			$note.find(".js-note-link").attr("href"), 
			$note.find(".js-note-title").text(), 
			$note.find(".js-note-text").text(), 
			function() {}, 
			function() {
				console.log("edit");
			}
		);
	})

$(".js-view").on("click", function() {
	$(".noteview")
		.removeClass("noteview_grid noteview_column noteview_list")
		.addClass("noteview_" + $(this).attr("data-view"));
});
$(".js-noteform-text").on("keyup", function() {
	var height = $(this).prop("scrollHeight");
	console.log(height);
	console.log($(this).height());
	if (height > $(this).height()) {
		$(this).css("height", height);
		console.log("");
	}
});