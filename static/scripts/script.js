(function() {

  var $ = jQuery;

  var submitSearch = function() {

    $('body').removeClass('hide-plants show-results');
    generate();

    $.ajax({
      url: '/search',
      dataType: 'json',
      method: 'post',
      data: $('.main-search-form').serialize(),
      success: renderResults
    });
    return false;
  };

  var renderResults = function(data) {
    $('.error').html('');

    if (data.users.length < 1) {
      $('.error').html('<div class="error-message"><strong>✖<strong> I\'m afraid the landscape is barren. Perhaps you need to plant more seeds.</div>');
    }

    var tmpl = _.template($('#results-tmpl').html());

    setTimeout(function() {
      $('body').addClass('hide-plants show-results');
    }, 4000);
    $('#the-people').html(tmpl({ users: _.sortBy(data.users, 'score').reverse() }));
  };

  var bindEvents = function() {
    $('form').on('submit', submitSearch);
  };

  $(document).ready(function() {
    bindEvents();
  });

})();
