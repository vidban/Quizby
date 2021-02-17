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
    let numQns = parseInt($("#num-questions").text());
    startTimer(60 * numQns, display);
  });

  $(document).on("click", "#user-statistics-tabs a", function (e) {
    e.preventDefault();
    $(this).tab("show");
  });

  const formatDate = (date) => {
    let d = new Date(date),
      month = "" + (d.getMonth() + 1),
      day = "" + d.getDate(),
      year = d.getFullYear();

    if (month.length < 2) month = "0" + month;
    if (day.length < 2) day = "0" + day;
    return [year, month, day].join("-");
  };

  const getChartData = async (testId) => {
    res = await axios.get(`/api/chartdata/${testId}`);
    data = res.data;
    for (d of data) {
      dTaken = d["date-taken"];
      d["date-taken"] = formatDate(dTaken);
    }
    return data;
  };

  $(document).on("click", "#chart-button", async (e) => {
    let testName = $(e.target).text();
    let testId = $(e.target).prev("#chart-quiz-id").text();
    $("#chart").text(testName);

    am4core.useTheme(am4themes_animated);

    let chart = am4core.create("chart", am4charts.XYChart);

    chart.data = await getChartData(testId);

    // Set input format for the dates
    chart.dateFormatter.inputDateFormat = "MM-dd-yyyy";

    // Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

    // Create series
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "score(%)";
    series.dataFields.dateX = "date-taken";
    series.tooltipText = "{score(%)}";
    series.strokeWidth = 2;
    series.minBulletDistance = 15;

    // Drop-shaped tooltips
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.strokeOpacity = 0;
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.label.minWidth = 40;
    series.tooltip.label.minHeight = 40;
    series.tooltip.label.textAlign = "middle";
    series.tooltip.label.textValign = "middle";

    // Make bullets grow on hover
    var bullet = series.bullets.push(new am4charts.CircleBullet());
    bullet.circle.strokeWidth = 2;
    bullet.circle.radius = 4;
    bullet.circle.fill = am4core.color("#fff");

    var bullethover = bullet.states.create("hover");
    bullethover.properties.scale = 1.3;

    // Make a panning cursor
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.behavior = "panXY";
    chart.cursor.xAxis = dateAxis;
    chart.cursor.snapToSeries = series;

    // Create vertical scrollbar and place it before the value axis
    chart.scrollbarY = new am4core.Scrollbar();
    chart.scrollbarY.parent = chart.leftAxesContainer;
    chart.scrollbarY.toBack();

    // Create a horizontal scrollbar with previe and place it underneath the date axis
    chart.scrollbarX = new am4charts.XYChartScrollbar();
    chart.scrollbarX.series.push(series);
    chart.scrollbarX.parent = chart.bottomAxesContainer;

    dateAxis.keepSelection = true;
  });
}
