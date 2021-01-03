$(document).on("change", "#mult_choice", function () {
  // if (this.checked) {
  //   $("#text_answer").parent().hide();
  //   $("label[id^=answer]").parent().show();
  // } else {
  $("#text_answer").parent().toggle();
  $("label[id^=answer]").parent().toggle();
  // }
});
