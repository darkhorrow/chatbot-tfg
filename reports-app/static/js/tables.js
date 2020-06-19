$(document).ready(function() {
    var oLanguage = "http://cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json";

    if($('#table').length) {
        var table = $('#table').DataTable({
            "language": { "url": oLanguage }
        });

        $('#table').on('click', 'tbody tr', function() {
            window.location.href = 'report/' + table.row(this).data()[1];
        })

        $('#table tbody tr').hover(function(){
            $(this).addClass('bg-light');
        }, function(){
            $(this).removeClass('bg-light');
        });
    }

    if($('#questions-table').length) {
        var table = $('#questions-table').DataTable({
            "language": { "url": oLanguage }
        });
    }

    if($('#rephrase-table').length) {
        var table = $('#rephrase-table').DataTable({
            "language": { "url": oLanguage }
        });
    }

    if($('#misunderstand-table').length) {
        var table = $('#misunderstand-table').DataTable({
            "language": { "url": oLanguage }
        });
    }

 });