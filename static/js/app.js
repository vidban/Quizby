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

  $(document).on("change", "#search-question-by", () => {
    if ($("#search-question-by").val() === "Category") {
      $("#questions #search").attr("placeholder", "Enter category...");
    } else {
      $("#questions #search").attr("placeholder", "Enter term...");
    }
  });

  const startTimer = (duration, display) => {
    let timer = duration,
      minutes,
      seconds;
    let refresh = setInterval(() => {
      minutes = parseInt(timer / 60, 10);
      seconds = parseInt(timer % 60, 10);

      minutes = minutes < 10 ? "0" + minutes : minutes;
      seconds = seconds < 10 ? "0" + seconds : seconds;

      let output = minutes + " : " + seconds;
      display.text(output);

      if (--timer < 0) {
        display.text("Time's Up!");
        setTimeout(() => {
          $("#submit-test").click();
        }, 2000);
        clearInterval(refresh); // exit refresh loop
        let music = $("#over_music")[0];
        music.play();
      }
    }, 1000);
  };

  $(document).on("click", "#start-quiz", () => {
    let display = $(".test #time");
    $("#start-quiz").toggleClass("hidden");
    $("#test-questions-form").toggleClass("hidden");
    startTimer(10, display);
  });

  $(document).on("click", "#user-statistics-tabs a", function (e) {
    e.preventDefault();
    console.log($(this));
    $(this).tab("show");
  });
}
