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

////////////////////////
// ON TOGGLE FUNCTION //
////////////////////////
$(".auto_fulfill-btn").on("change", function() {
  var sku_id = $(this)
    .parent()
    .parent()
    .siblings(".sku_id")
    .html();

  if (this.checked) {
<<<<<<< HEAD
    console.log(`on for ${sku_id}`);
    // auto_fulfill -> True
  } else {
    console.log(`off for ${sku_id}`);
    // auto_fulfill -> False
=======
    $.ajax({
      type: "GET",
      url: "../orders/fulfill/" + sku_id + "/on"
    });
  } else {
    $.ajax({
      type: "GET",
      url: "../orders/fulfill/" + sku_id + "/on"
    });
>>>>>>> d4b10fbffa71d7b36b6c0f98b9df99b7e7d889d8
  }
});

////////////////
// Log Button //
////////////////
$(".btn-log ").click(function() {
  var order_id = $(this)
    .parent()
    .siblings(".order_id")
    .html();

  // HARDCODED URL (SWITCHING SHEETS MONTHLY OMEGALUL)
  var sheets_url =
    "https://docs.google.com/spreadsheets/d/1kQHu41vQ6QL1_5k-hbtPi20AI6YOKfx0lcBTlDtshD8/edit?ts=5b1455d8#gid=1703849860";

  console.log(`logging order ${order_id} to ${sheets_url}`);
  $.ajax({
    type: "GET",
    url: "orders/upload/" + order_id + "/" + sheets_url
  }).done(function(msg) {
    if (msg.status == "error") {
      alert("Error Logging Data to Google Sheets");
    }
    // TODO:
    // Change order.uploaded to true
    console.log(`succesfully logged order ${order_id}`);
    location.reload();
  });
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

$(".fulfill-button").click(function() {
  $('.fulfill-settings').slideToggle(500);
});