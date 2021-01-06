{
  let categories = [];
  $(document).on("change", "#mult_choice", function () {
    if ($("input[id^=mult_choice]:checked").val() === "f") {
      $("#text_answer").parent().toggle();
      $("label[id^=answer]").parent().toggle();
    } else if ($("input[id^=mult_choice]:checked").val() === "mc") {
      $("#text_answer").parent().toggle();
      $("label[id^=answer]").parent().toggle();
    }
  });

  //  autocomplete for question form
  $(document).on(
    "click",
    "div#new-question input#autocomplete",
    async function () {
      res = await axios.get("/api/categories");
      categories = res.data;
      let $dlist = $("#list-of-categories");
      for (c of categories) {
        $("<option>").text(c).appendTo($dlist);
      }
    }
  );

  $(document).on("blur", "div#new-question input#autocomplete", function () {
    $("#list-of-categories").empty();
  });

  // remove flash messages
  window.setTimeout("document.getElementById('alert').remove();", 1500);
}
