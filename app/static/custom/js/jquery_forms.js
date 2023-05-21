(function ($) {
	"use strict";
    /*-------------------------------------
        Date Picker
    -------------------------------------*/
    if ($.fn.datepicker !== undefined) {
        // $('.air-datepicker').datepicker({
        //     language: {
        //         days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        //         daysShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        //         daysMin: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
        //         months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        //         monthsShort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        //         today: 'Today',
        //         clear: 'Clear',
        //         dateFormat: 'dd/mm/yyyy',
        //         firstDay: 0
        //     }
        // });
        $(".air-datepicker").datepicker({
            dateFormat: 'dd/mm/yyyy',
            changeMonth: true,
            changeYear: true,
            setLocale: 'en'
        });
    };

    /*-------------------------------------
        Manage avatar upload
        var btnCust = '<button type="button" class="btn btn-secondary" title="Add picture tags" onclick="alert(\'Call your custom code here.\')"><i class="bi-tag"></i></button>'; 
    -------------------------------------*/
    $("#passport_photo").fileinput({
        overwriteInitial: true,
        maxFileSize: 1500,
        showClose: false,
        showCaption: false,
        showBrowse: false,
        browseOnZoneClick: true,
        removeLabel: ' Remove.',
        removeIcon: '<i class="bi-x-lg"></i>',
        removeTitle: 'Cancel or reset changes',
        elErrorContainer: '#kv-avatar-errors-2',
        msgErrorClass: 'alert alert-block alert-danger',
        defaultPreviewContent: `<img src="static/img/default_prof.jpg" style="background: transparent;" alt="Profile Photo"><br><br><h6 class="text-muted"><i class="fas fa-cloud-upload-alt mg-l-10"></i> Upload</h6>`,
        layoutTemplates: { main2: '{preview} {remove} {browse}' }, // layoutTemplates: {main2: '{preview} ' +  btnCust + ' {remove} {browse}'},
        allowedFileExtensions: ["jpg", "png"]
    });

    /*-------------------------------------
        All files
    -------------------------------------*/
    $("#files").fileinput({
        overwriteInitial: true,
        maxFileSize: 1500,
        showClose: false,
        showCaption: false,
        showBrowse: false,
        browseOnZoneClick: true,
        removeLabel: ' Remove.',
        removeIcon: '<i class="bi-x-lg"></i>',
        removeTitle: 'Cancel or reset changes',
        elErrorContainer: '#kv-files-errors-2',
        msgErrorClass: 'alert alert-block alert-danger',
        defaultPreviewContent: `<img src="static/img/file_upload.png" style="background: transparent;" alt="File Upload"><br><br><h6 class="text-muted"><i class="fas fa-cloud-upload-alt mg-l-10"></i> Upload</h6>`,
        layoutTemplates: { main2: '{preview} {remove} {browse}' }, // layoutTemplates: {main2: '{preview} ' +  btnCust + ' {remove} {browse}'},
        allowedFileExtensions: ["jpg", "png", "pdf", "docx", "csv"]
    });

    /*-------------------------------------
        All Checkbox Checked
    -------------------------------------*/
    $(".checkAll").on("click", function () {
        $(this).parents('.table').find('input:checkbox').prop('checked', this.checked);
    });

    function getIp(callback) {
        fetch('/get_location')
            .then((resp) => resp.json())
            .catch((error) => {
                console.error(error);
                return {
                    country: 'ke',
                };
            })
            .then((resp) => callback(resp.country));
    };

    let utilsScriptCDN = "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js";
    let phoneInputField = document.querySelector('#phone');
    if (phoneInputField !== null) {
        window.intlTelInput(phoneInputField, {
            initialCountry: "ke",
            geoIpLookup: getIp,
            utilsScript: utilsScriptCDN,
        });
    };
})(jQuery);
