$(document).ready(function() {
  var d = new Date();
  var h = d.getUTCHours();
  var m = d.getUTCMinutes();
  var ampm = h >= 12 ? 'pm' : 'am';
  h = h % 12;
  if (h == 0) h = 12;
  var utc_string = h + ':' + (m < 10 ? '0' : '') + m + ampm;
  $('#utcnow').html(utc_string);
});
