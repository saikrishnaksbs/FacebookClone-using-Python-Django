
$(document).on("submit", "#post-form", function (e) {
  e.preventDefault();
  var username = $("#username").val();
  var friendsname = $("#friendsname").val();
  console.log(username, friendsname);

  $.ajax({
    type: "POST",
    url: "/tomessage",
    data: {
      username: $("#username").val(),
      friendsname: $("#friendsname").val(),
      message: $("#message").val(),
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (data) {
      console.log(data.message);
    },
  });
  document.getElementById("message").value = "";
});

$(document).ready(function () {
  setInterval(function () {
    var friendsname = $("#friendsname").val();
    console.log(friendsname)
    console.log()
    $.ajax({
      type: "GET",
      url: "/getmessage/" + friendsname,
      success: function (response) {
        console.log(response);
        $("#display").empty();
        for (var chat in response.chats) {
          var meessagedetails =
            "<b>" + `<div class="allmsgs">`+
            response.chats[chat].sendersname +`
            </b><p>` +
            response.chats[chat].message +
            "</p>" +
            "<br><br>";+
            `</div>`
          $("#display").append(meessagedetails);
        }
      },
    });
  }, 1000);
});

$('.friendbutton').click(function () {
  var friendname = $(this).attr("friendname");
  var friendid = $(this).attr("friendid")
  console.log(friendname, friendid)
  $.ajax({
    url: '/sendmessage',
    type: 'POST',
    data: { 'friendname': friendname, 'friendid': friendid, csrfmiddlewaretoken: '{{ csrf_token }}' },
    dataType: 'json',
    success: function (response) {
      console.log(response.message)
      $('.friendbuttons' + friendname).text(response.message);
    }
  });
});