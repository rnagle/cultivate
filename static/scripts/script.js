(function() {

  var $ = jQuery;

  var submitSearch = function() {

    $('body').removeClass('hide-plants');
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
    var tmpl = _.template($('#results-tmpl').html());
    $('#results ul').html(tmpl({ users: data.users }));
    setTimeout(function() {
      $('body').addClass('hide-plants show-results');
    }, 4000);
  };

  var bindEvents = function() {
    $('form').on('submit', submitSearch);
  };

  $(document).ready(function() {
    bindEvents();
  });

})();
