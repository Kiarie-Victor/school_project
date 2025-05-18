(function($) {
    $(document).ready(function() {
        function updateMemberDropdown() {
            const faculty = $('#id_faculty').val();
            const year = $('#id_year_of_study').val();

            if (faculty && year) {
                $.ajax({
                    url: '/accounts/filter-members/',
                    data: {
                        faculty: faculty,
                        year: year
                    },
                    success: function(data) {
                        const memberSelect = $('#id_member');
                        memberSelect.empty();
                        memberSelect.append('<option value="">---------</option>');
                        $.each(data.members, function(index, member) {
                            memberSelect.append(
                                $('<option></option>').attr('value', member.id).text(member.name)
                            );
                        });
                    }
                });
            }
        }

        $('#id_faculty, #id_year_of_study').change(updateMemberDropdown);
    });
})(django.jQuery);
