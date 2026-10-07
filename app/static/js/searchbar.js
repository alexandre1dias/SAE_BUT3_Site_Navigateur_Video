$(document).ready(function () {
    function resetSearch() {
        $('#search-results .dropdown-item, #search-results .dropdown-divider').remove();
    }
    resetSearch();
    $('#search').on('keyup', function () {
        var value = $(this).val();
        if (value.length == 0) {
            $('#search-results').dropdown('hide');
            return;
        }
        $.ajax({
            url: '/api/search',
            data: {
                'term': value
            },
            success: function (data) {
                resetSearch();
                var results = data;

                for (let key of Object.keys(results)) {
                    let cat = $(`#search-results-${key}`);
                    if (results[key].length > 0) {
                        cat.show();
                        cat.after('<div class="dropdown-divider"></div>');
                        results[key].forEach((result) => {
                            cat.after(`<a class='dropdown-item' href='${result.url}'>${result.label}</a>`)
                        });
                    } else {
                        cat.hide();
                    }
                }

                if ($('#search-results').children().last().hasClass('dropdown-divider')) {
                    $('#search-results').children().last().remove();
                }
                
                $('#search-results').dropdown('show');
            }
        });
    });
});