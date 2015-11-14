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

    if (data.users.length < 1)
      $('.error').html('<h2>No results found!</h2>');

    var tmpl = _.template($('#results-tmpl').html());
    $('#results ul').html(tmpl({ users: data.users }));
    setTimeout(function() {
      $('body').addClass('hide-plants show-results');
    }, 4000);
    $('#results ul').html(tmpl({ users: _.sortBy(data.users, 'score').reverse() }));
  };

  var bindEvents = function() {
    $('form').on('submit', submitSearch);
  };

  $(document).ready(function() {
    bindEvents();
  });

})();
