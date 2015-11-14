(function() {

  var $ = jQuery;

  var submitSearch = function() {

    // temp for ui
    $('body').addClass('show-results');
    generate();
    setTimeout(function() {
      $('body').addClass('hide-plants');
    }, 5000)

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
    var tmpl = _.template($('#results-tmpl').html());
    $('#results ul').html(tmpl({ users: data.users }));
    $('body').addClass('show-results');
  };

  var bindEvents = function() {
    $('form').on('submit', submitSearch);
  };

  $(document).ready(function() {
    bindEvents();
  });

})();
