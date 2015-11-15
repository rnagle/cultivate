(function() {

  var $ = jQuery;

  var submitSearch = function() {
    if (!validateSearch()) {
      $('body').addClass('hide-plants show-results')
      $('.error').html('<div class="error-message"><strong>✖</strong> Sorry, we\'ll need more seeds (keywords) to yield crops (results).</div>');
      return false;
    }

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

  var validateSearch = function() {
    var valid = true;
    $('.main-search-form input').each(function() {
      if ($(this).val().trim() == '')
        valid = false;
    });
    return valid;
  };

  var renderResults = function(data) {
    $('.error').html('');

    if (data.users.length < 1) {
      $('.error').html('<div class="error-message"><strong>✖</strong> I\'m afraid the landscape is barren. Perhaps you need to plant more seeds.</div>');
    }

    var tmpl = _.template($('#results-tmpl').html());
    $('#the-people').html(tmpl({ users: _.sortBy(data.users, 'score').reverse() }));

    setTimeout(function() {
      $('body').addClass('hide-plants show-results');
      $('html, body').animate({
          scrollTop: $("#results").offset().top
      }, 2000);
    }, 4000);

  };

  var bindEvents = function() {
    $('form').on('submit', submitSearch);

    $('.queries button').on('click', function() {
      city = $(this).data("city");
      term = $(this).data("terms");
      $("input[name='city']").val(city);
      $("input[name='term[]']").val(term);
      $('form').submit();
    });
  };

  bindEvents();

})();
