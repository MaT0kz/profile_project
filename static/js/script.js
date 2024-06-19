let heart = document.querySelector('.heart');
let likesNumber = document.querySelector('.likes-number');

heart.onclick = function () {
    if (heart.classList.contains('added')) {
        likesNumber.textContent--;
    } else {
        likesNumber.textContent++;
    }
    heart.classList.toggle('added');
};

let commentForm = document.querySelector('.comment-form');
let commentList = document.querySelector('.comment-list');
let commentField = document.querySelector('.comment-field');

commentForm.onsubmit = function (evt) {
    evt.preventDefault();
    let newComment = document.createElement('li');
    newComment.classList.add('user-comment');
    newComment.textContent = commentField.value;
    commentField.value = '';
    commentList.append(newComment);
};