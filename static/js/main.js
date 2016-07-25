$('.js-person-search').selectize({
  maxItems: 1,
  persist: false,
  create: function(text) {
    var form = $('<form>', {action:'/people', method: 'POST'});
    form.append($('<input>', {name:'name', value:text}));
    form.submit();
  },
  onItemAdd: function(value) {
    window.location = '/people/' + value;
  },
  load: function(query, callback) {
    if (!query.length) return callback();
    $.ajax({
      url: '/people.json',
      data: { query: query },
      error: function() { callback() },
      success: function(res) {
        var rows = $.map(res.results.slice(0, 10), function(person) {
          return {
            value: person.id,
            text: person.name
          };
        });
        callback(rows);
      }
    });
  }
});

$('.js-role').selectize({
  selectOnTab: true,
  create: function(text, callback) {
    $.ajax({
      url: '/roles.json',
      method: 'POST',
      data: { name: text },
      success: function(r) {
        callback({
          value: r.result.id,
          text: r.result.name
        });
      }
    });
  }
});

