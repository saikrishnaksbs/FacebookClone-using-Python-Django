$('.friendbutton').click(function () {
  var friendname = $(this).attr("friendname");
  var friendid = $(this).attr("friendid")
  console.log(friendname, friendid)
  $.ajax({
    url: '/removefriend',
    type: 'POST',
    data: { 'friendname': friendname, 'friendid': friendid, csrfmiddlewaretoken: '{{ csrf_token }}' },
    dataType: 'json',
    success: function (response) {
      console.log(response.message)
      $('.friendbuttons' + friendname).text(response.message);
    }
  });
});


$('.acceptbutton').click(function () {
  var friendid = $(this).attr("friendid");
  var friendname = $(this).attr("friendname");
  console.log(friendid)
  $.ajax({
    url: '/acceptrequest',
    type: 'POST',
    data: { 'friendid': friendid, 'friendname': friendname, csrfmiddlewaretoken: '{{ csrf_token }}' },
    dataType: 'json',
    success: function (response) {
      console.log(response.message)
      $('.accept' + friendid).text("");
      $('#stmt' + friendid).text(response.message);
    }
  });
});

$('.rejectbutton').click(function () {
  var friendid = $(this).attr("friendid");
  var friendname = $(this).attr("friendname");
  console.log(friendid)
  $.ajax({
    url: '/rejectrequest',
    type: 'POST',
    data: { 'friendid': friendid, 'friendname': friendname, csrfmiddlewaretoken: '{{ csrf_token }}' },
    dataType: 'json',
    success: function (response) {
      console.log(response.message)
      $('.accept' + friendid).text("");
      $('#stmt' + friendid).text(response.message);
    }
  });
});

$(document).ready(function () {
  $(".comment-form").on('keydown', function (event) {
    if (event.key === 'Enter') {
      var postid = $(this).attr("postid");
      var comment = $(".comment-text" + postid).val()
      console.log(postid, comment)
      event.preventDefault();
      $.ajax({
        type: "POST",
        url: '/postComment',
        data: {
          csrfmiddlewaretoken: "{{ csrf_token }}",
          comment: $(".comment-text" + postid).val(),
          'postid': postid
        },
        success: function (response) {
          console.log(response.comment)
          $(".cmmts" + postid).append(`<div class="allcomments">
            <div class="commenterimage">
              <img src="` + response.profileimg + `" width="50px" height="40px" />
            </div>
            <div class="commentername">
              <span>` + response.name + `</span>
            </div>
            <div>
            </div>
            <div class="commentbody" >
              ` + response.comment + `
            </div>
          </div>
          `);
          $('.comment-text' + postid).val('');
        }
      });
    }
  });
});

$('.like-button').click(function () {
  var postId = $(this).attr("data-post-id");
  var profileid = $(this).attr("data-userprofile-id");
  console.log(postId, profileid)
  $.ajax({
    url: '/like-post',
    type: 'POST',
    data: { 'post_id': postId, 'profile_id': profileid, csrfmiddlewaretoken: '{{ csrf_token }}' },
    dataType: 'json',
    success: function (response) {
      console.log(response.likes, response.post_id)
      $('#like-count-' + postId).text("liked by " + response.likes + " people");
      var button = $('#' + postId + profileid);
      if (button.css('color') === 'rgb(0, 0, 0)') {
        button.css('color', 'rgb(0, 0, 255)');
      } else {
        button.css('color', 'rgb(0, 0, 0)');
      }
    }
  });
});

$(document).ready(function () {
  $('#text-button').click(function () {
    var searchedbyid = $(this).attr("searchedby-id");
    var searchedid = $(this).attr("searched-id");
    var searchedname = $(this).attr("searchedname");
    console.log(searchedbyid, searchedid)
    $.ajax({
      url: '/addrequest',
      type: 'POST',
      data: { 'searchedbyid': searchedbyid, 'searchedid': searchedid, 'searchedname': searchedname, csrfmiddlewaretoken: '{{ csrf_token }}' },
      dataType: 'json',
      success: function (response) {
        if ($('#text-button').text() === 'Send request') {
          $('#text-button').text(response.response);
        } else {
          $('#text-button').text(response.response);
        }
      }
    });
  });
});

$(document).ready(function () {
  $('#follow').click(function () {
    var searchedbyid = $(this).attr("searchedby-id");
    var searchedid = $(this).attr("searched-id");
    var searchedname = $(this).attr("searchedname");
    console.log(searchedbyid, searchedid)
    $.ajax({
      url: '/follow',
      type: 'POST',
      data: { 'searchedbyid': searchedbyid, 'searchedid': searchedid, 'searchedname': searchedname, csrfmiddlewaretoken: '{{ csrf_token }}' },
      dataType: 'json',
      success: function (response) {
        $('#follow').text(response.msg);
        $('#followers').text(response.followers_count + " Followers");
      }
    });
  });
});

$(document).ready(function () {
  $('#unfollow').click(function () {
    var searchedbyid = $(this).attr("searchedby-id");
    var searchedid = $(this).attr("searched-id");
    var searchedname = $(this).attr("searchedname");
    console.log(searchedbyid, searchedid)
    $.ajax({
      url: '/unfollow',
      type: 'POST',
      data: { 'searchedbyid': searchedbyid, 'searchedid': searchedid, 'searchedname': searchedname, csrfmiddlewaretoken: '{{ csrf_token }}' },
      dataType: 'json',
      success: function (response) {
        $('#unfollow').text(response.msg);
        $('#followers').text(response.followers_count + " Followers");
      }
    });
  });
});

const searchIcon = document.getElementById("search-icon");
const homeIcon = document.getElementById("home-icon");
const msgIcon = document.getElementById("msg-icon");
const friendrequestIcon = document.getElementById("friendrequest-icon");
const profileIcon = document.getElementById("profile-icon");
const searchForm = document.getElementById("search-form");


searchIcon.addEventListener("click", function () {
  if (searchForm.style.display === "none") {
    searchForm.style.display = "block";
    homeIcon.style.display = "none";
    msgIcon.style.display = "none";
    friendrequestIcon.style.display = "none";
    profileIcon.style.display = "none";

  } else {
    searchForm.style.display = "none";
    homeIcon.style.display = "block";
    msgIcon.style.display = "block";
    friendrequestIcon.style.display = "block";
    profileIcon.style.display = "block";
  }
});