$(document).on("change", "#mult_choice", function () {
  if ($("input[id^=mult_choice]:checked").val() === "f") {
    $("#text_answer").parent().toggle();
    $("label[id^=answer]").parent().toggle();
  } else if ($("input[id^=mult_choice]:checked").val() === "mc") {
    $("#text_answer").parent().toggle();
    $("label[id^=answer]").parent().toggle();
  }
});
