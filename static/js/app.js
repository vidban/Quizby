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
    $(this).tab("show");
  });

  $(document).on("click", "#chart-button", (e) => {
    let testName = $(e.target).text();
    $("#chart").text(testName);
    am4core.useTheme(am4themes_animated);

    let chart = am4core.create("chart", am4charts.XYChart);

    chart.data = [
      {
        "date-taken": "2/2/2021",
        "score(%)": 50,
      },
      {
        "date-taken": "2/5/2021",
        "score(%)": 75,
      },
      {
        "date-taken": "2/7/2021",
        "score(%)": 100,
      },
      {
        "date-taken": "2/9/2021",
        "score(%)": 25,
      },
      {
        "date-taken": "2/11/2021",
        "score(%)": 75,
      },
    ];

    let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "date-taken";
    categoryAxis.renderer.grid.template.location = 0;
    categoryAxis.renderer.minGridDistance = 30;

    categoryAxis.renderer.labels.template.adapter.add("dy", (dy, target) => {
      if (target.dataItem && target.dataItem.index & (2 == 2)) {
        return dy + 25;
      }
      return dy;
    });

    let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

    let series = chart.series.push(new am4charts.ColumnSeries());
    series.dataFields.valueY = "score(%)";
    series.dataFields.categoryX = "date-taken";
    series.name = "Score";
    series.columns.template.tooltipText = "{categoryX} : [bold]{valueY}[/]";
    series.columns.template.fillOpacity = 0.8;

    let columnTemplate = series.columns.template;
    columnTemplate.strokeWidth = 2;
    columnTemplate.strokeOpacity = 1;
  });
}
