const handleInputPaymentMethod = (element) => {
    if (element.value == 0) {
        $('#id_reference_number').show()
        $('#id_reference_number').attr('required', true)
    } else {
        $('#id_reference_number').hide()
        $('#id_reference_number').attr('required', false)
    }
}

const handleInputUpdatePaymentMethod = (element) => {
    if (element.value == 0) {
        $('#id_update_reference_number').show()
        $('#id_update_reference_number').attr('required', true)
    } else {
        $('#id_update_reference_number').hide()
        $('#id_update_reference_number').attr('required', false)
    }
}