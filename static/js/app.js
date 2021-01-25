{
  let categories = [];
  $(document).on("change", "#mult_choice", function () {
    if ($("input[id^=mult_choice]:checked").val() === "f") {
      $("#text_answer").parent().toggle();
      $("table[id^=answer_] input").removeAttr("required");
      $("label[id^=answer]").parent().toggle();
    } else if ($("input[id^=mult_choice]:checked").val() === "mc") {
      $("#text_answer").parent().toggle();
      $("label[id^=answer]").parent().toggle();
    }
  });

  //  autocomplete for question form
  $(document).on("click", "input#autocomplete", async function () {
    if ($("input[id^=mult_choice]:checked").val() === "mc") {
      $("table[id^=answer_] tr:first-child input").prop("required", true);
    }
    res = await axios.get("/api/categories");
    categories = res.data;
    let $dlist = $("#list-of-categories");
    for (c of categories) {
      $("<option>").text(c).appendTo($dlist);
    }
  });

  $(document).on("blur", "input#autocomplete", function () {
    $("#list-of-categories").empty();
  });
}
