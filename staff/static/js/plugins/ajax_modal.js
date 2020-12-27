$(document).ready(function(){


  var loadForm = function() {
    var btn = $(this);
    console.log(btn.attr("href"));
    $.ajax({
      url: btn.attr("href"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal").modal("show");
      },
      success: function (data) {
        $("#modal .modal-content").html(data.html_form);
      }
    });
    return false;
  };

  var saveForm = function() {
    var form = $(this);
    var target = form.attr("data-target")
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $(target).html(data.list);
          $("#modal").modal("hide");
        }
        else {
          $("#modal .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  var dateMonthQuery = function() {
    var form = $(this);
    var target = form.attr("data-target");
    var option = form.attr("data-option");
    $.ajax({
      url: form.attr("action"),
      data: form.serialize() + "&option=" + option,
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $(target).html(data.list);
        }
      }
    });
    return false;
  }

  $("body").on('click', '.js-load-form', loadForm);
  $("body").on('submit', '.js-save-form', saveForm);
  $("body").on('submit', '.js-date-month', dateMonthQuery)
})
