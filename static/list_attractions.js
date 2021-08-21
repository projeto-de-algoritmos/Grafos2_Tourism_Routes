var selectAttractionModal = document.getElementById('selectAttractionModal')
selectAttractionModal.addEventListener('show.bs.modal', function (event) {
// Button that triggered the modal
var button = event.relatedTarget
// Extract info from data-bs-* attributes
var attraction_id = button.getAttribute('data-bs-attraction-id')
var attraction_name = button.getAttribute('data-bs-attraction-name')
var modalTitle = selectAttractionModal.querySelector('.modal-title')

var modalContent = selectAttractionModal.querySelector('.modal-body')

var confirmButton = document.getElementsByClassName('confirm')
confirmButton[0].setAttribute('id', attraction_id)

modalTitle.textContent = 'Selecionar atração ' + attraction_name
modalContent.textContent = 'Deseja selecionar a atração ' + attraction_name + '?'
})

var removeAttractionModal = document.getElementById('removeAttractionModal')
removeAttractionModal.addEventListener('show.bs.modal', function (event) {
// Button that triggered the modal
var button = event.relatedTarget
// Extract info from data-bs-* attributes
var attraction_id = button.getAttribute('data-bs-attraction-id')
var attraction_name = button.getAttribute('data-bs-attraction-name')
var modalTitle = removeAttractionModal.querySelector('.modal-title')

var modalContent = removeAttractionModal.querySelector('.modal-body')

var confirmButton = document.getElementsByClassName('cancel')
confirmButton[0].setAttribute('id', attraction_id)

modalTitle.textContent = 'Remover atração ' + attraction_name
modalContent.textContent = 'Deseja remover a atração ' + attraction_name + '?'
})

$('.confirm').click(function() {
    var attraction_id = $(this).attr('id');
    window.location = '/attractions/select/' + attraction_id
});

$('.cancel').click(function() {
    var attraction_id = $(this).attr('id');
    window.location = '/attractions/remove/' + attraction_id
});