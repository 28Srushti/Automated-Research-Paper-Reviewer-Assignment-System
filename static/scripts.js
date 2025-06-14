// static/js/scripts.js

$(document).ready(function(){
    // Check if the showModal div is present and has data-show attribute set to true
    if ($('#showModal').data('show')) {
        $('#messageModal').modal('show');
    }
});
