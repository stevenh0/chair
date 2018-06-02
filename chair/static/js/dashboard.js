$(document).ready(function() {
  $("#stockTable").DataTable({ order: [[0, "desc"]] });
});
$(document).ready(function() {
  $("#pendingTable").DataTable({ order: [[0, "desc"]] });
});
$(document).ready(function() {
  $("#reportTable").DataTable({ order: [[0, "desc"]] });
});

$(document).ready(function() {
  $("#completeTable").DataTable({ order: [[0, "desc"]] });
});

// ON TOGGLE FUNCTION
/////////////////////
$(".on").on("change", function() {
  var sku_id = $(this)
    .parent()
    .parent()
    .siblings(".sku_id")
    .html();

  if (this.checked) {
    console.log(`on & ${sku_id}`);
  } else {
    console.log(`off & ${sku_id}`);
  }
});

// Accept Button
$(".btn-accept ").click(function(e) {
  e.preventDefault();
  var order_id = $(this)
    .parent()
    .siblings(".order_id")
    .html();
  $.ajax({
    type: "GET",
    url: "../orders/accept/" + order_id + "/",
    success: function() {
      // On Success
    },
    error: function() {
      // cry for help
    }
  }).done(function(msg) {
    location.reload();
    console.log(msg);
  });
});

// Details Button
$(".btn-details ").click(function() {
  var order_id = $(this)
    .parent()
    .siblings(".order_id")
    .html();
  console.log("details with... " + order_id);
  // $.ajax({
  //   type: 'GET',
  //   url: '../orders/accept/' + order_id + '/',
  //   success: function () {
  //     console.log('success')
  //   },
  //   error: function () {
  //     console.log('error')
  //   }
  // });
});

// Send order via newegg
$(".btn-send ").click(function() {
  var order_id = $(this)
    .parent()
    .siblings(".order_id")
    .html();
  $.ajax({
    type: "GET",
    url: "../orders/newegg_fulfill/" + order_id + "/"
  }).done(function(msg) {
    location.reload();
    console.log(msg);
  });
});

// Request new tracking report to grab tracking ids
$(".btn-report ").click(function() {
  $.ajax({
    type: "GET",
    url: "../orders/get_report/"
  }).done(function(msg) {
    location.reload();
    console.log(msg);
  });
});

// Parse tracking report to get tracking IDs
$(".btn-parse-report ").click(function() {
  var report_id = $(this)
    .parent()
    .siblings(".report_id")
    .html();
  console.log(report_id);
  $.ajax({
    type: "GET",
    url: "../orders/parse_report/" + report_id + "/",
    error: function() {
      alert("Report not ready, or did not contain necessary info");
    }
  }).done(function(msg) {
    if (msg.status == "error") {
      alert("Report not ready, or did not contain necessary info");
    } else {
      location.reload();
    }
  });
});

// Update tracking ID on bestbuy
$(".btn-bestbuy-tracking ").click(function() {
  var order_id = $(this)
    .parent()
    .siblings(".order_id")
    .html();
  $.ajax({
    type: "GET",
    url: "../orders/update_tracking/" + order_id + "/"
  }).done(function(msg) {
    location.reload();
    console.log(msg);
  });
});
