Comments = window.Comments || {};

(function(exports, $) {
    /* Template string for rendering success or error messages. */
    var alertMarkup = (
        '<div class="alert alert-{class} alert-dismissable">' +
        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
        '<strong>{title}</strong> {body}</div>'
        );

    /* Create an alert element. */
    function makeAlert(alertClass, title, body) {
        var alertCopy = (alertMarkup
        .replace('{class}', alertClass)
        .replace('{title}', title)
        .replace('{body}', body));
        return $(alertCopy);
    }

    /* Retrieve the values from the form fields and return as an
    object. */
    function getFormData(form) {
        return {
            'name': form.find('input#name').val(),
            'email': form.find('input#email').val(),
            'url': form.find('input#url').val(),
            'body': form.find('textarea#body').val(),
            'entry_id': form.find('input[name=entry_id]').val()
        }
    }

    function bindHandler() {
        /* When the comment form is submitted, serialize the form data as JSON and POST it to the API. */
        $('form#comment-form').on('submit', function() {
            var form = $(this);
            var formData = getFormData(form);
            alert(formData);
            var request = $.ajax({
                url: "form.attr('action')",
                dataType: "json",
                contentType: "application/json",
                type: 'POST',
                data: JSON.stringify(formData)
            });
            
            request.success(function(data) {
                alertDiv = makeAlert('success', 'Success', 'your comment was posted.');
                form.before(alertDiv);
                form[0].reset();
            });

            request.fail(function() {
                alertDiv = makeAlert('danger', 'Error', 'your comment was not posted.');
                form.before(alertDiv);
            });

            return false;
        });

    }
    exports.bindHandler = bindHandler;
})(Comments, jQuery);