document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll(".caret").forEach(function(toggler) {
        toggler.addEventListener("click", function() {
            this.parentElement.querySelector(".nested").classList.toggle("active");
            this.classList.toggle("caret-down");
        });
    });

    document.querySelectorAll(".nested li").forEach(function(version) {
        version.addEventListener('click', function() {
            const versionUuid = this.getAttribute('data-version-uuid');
            fetch(`/3Dmodels/version_data/${versionUuid}/`)
                .then(response => response.json())
                .then(data => {
                    const detailsHtml = `<div>
                                           <h1>${data.name}</h1>
                                           <p>${data.description}</p>
                                           <p>Créé le : ${data.created_at}</p>
                                         </div>`;
                    document.getElementById('content-details').innerHTML = detailsHtml;
                })
                .catch(error => console.error('Error:', error));
        });
    });

    document.querySelectorAll(".btn-add-version").forEach(btn => {
        btn.addEventListener('click', function() {
            const varianteUuid = this.getAttribute('data-variante-uuid');
            document.querySelector("#versionForm").action = `/3Dmodels/variante/${varianteUuid}/add_version/`;
            document.getElementById("versionModal").style.display = "block";
        });
    });

    document.getElementById('btn-add-variante').addEventListener('click', function() {
        const modeleUuid = this.getAttribute('data-modele-uuid');
        document.querySelector("#addVarianteForm").action = `/3Dmodels/modele/${modeleUuid}/add_variante/`;
        document.getElementById('addVarianteModal').style.display = 'block';
    });
    
    
    document.querySelectorAll(".btn-edit-variante").forEach(btn => {
        btn.addEventListener('click', function() {
            const varianteUuid = this.getAttribute('data-variante-uuid');
            fetch(`/3Dmodels/variante/${varianteUuid}/edit_data/`)
                .then(response => response.json())
                .then(data => {
                    const form = document.querySelector("#varianteForm");
                    form.action = `/3Dmodels/variante/${varianteUuid}/edit/`;
                    form.querySelector("[name='name']").value = data.name;
                    form.querySelector("[name='description']").value = data.description;
    
                    const imageElement = form.querySelector("img#varianteImagePreview");
                    if(imageElement) { 
                        imageElement.src = data.image_url || 'chemin/vers/image/par/defaut.png';
                    }
    
                    document.getElementById("varianteModal").style.display = "block";
                })
                .catch(error => console.error('Error:', error));
        });
    });

    document.querySelectorAll(".btn-edit-version").forEach(btn => {
        btn.addEventListener('click', function() {
            const versionUuid = this.getAttribute('data-version-uuid');
            fetch(`/3Dmodels/version/${versionUuid}/edit_data/`)
                .then(response => response.json())
                .then(data => {
                    const form = document.querySelector("#versionForm");
                    form.action = `/3Dmodels/version/${versionUuid}/edit/`;
                    form.querySelector("[name='name']").value = data.name;
                    form.querySelector("[name='description']").value = data.description;
                    const imageElement = form.querySelector("img#versionImagePreview");
                    if(imageElement) { 
                        imageElement.src = data.image_url || 'chemin/vers/image/par/defaut.png';
                    }
                    document.getElementById("editVersionModal").style.display = "block";
                })
                .catch(error => console.error('Error:', error));
        });
    });
    

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    

    document.querySelectorAll('.btn-delete-variante').forEach(button => {
        button.addEventListener('click', function() {
            const varianteUuid = this.getAttribute('data-variante-uuid');
            if(confirm('Êtes-vous sûr de vouloir supprimer cette variante ?')) {
                fetch(`/3Dmodels/variante/${varianteUuid}/delete/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                }).then(response => {
                    if(response.ok) {
                        window.location.reload(); 
                    }
                }).catch(error => console.error('Error:', error));
            }
        });
    });

    document.querySelectorAll('.btn-delete-version').forEach(button => {
        button.addEventListener('click', function() {
            const versionUuid = this.getAttribute('data-version-uuid');
            if(confirm('Êtes-vous sûr de vouloir supprimer cette version ?')) {
                fetch(`/3Dmodels/version/${versionUuid}/delete/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                }).then(response => {
                    if(response.ok) {
                        window.location.reload(); 
                    }
                }).catch(error => console.error('Error:', error));
            }
        });
    });

    document.querySelectorAll(".modal .close").forEach(span => {
        span.onclick = function() {
            this.closest(".modal").style.display = "none";
        }
    });

    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = "none";
        }
    }

    document.querySelectorAll('.btn-toggle-favorite').forEach(button => {
        const versionUuid = button.getAttribute('data-version-uuid');
        button.addEventListener('click', function(event) {
            event.stopPropagation();
            let isAnotherFavorite = document.querySelector('.star-filled') && !button.classList.contains('star-filled');
            if (isAnotherFavorite && !confirm('Une version est déjà en favori. Voulez-vous changer le favori ?')) {
                return;
            }
            fetch(`/3Dmodels/toggle_favorite/${versionUuid}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
            })
            .then(response => response.json())
            .then(data => {
                document.querySelectorAll('.btn-toggle-favorite').forEach(btn => {
                    btn.classList.remove('star-filled');
                    btn.classList.add('star-empty');
                });
                button.classList.toggle('star-filled');
                button.classList.toggle('star-empty');
            })
            .catch(error => console.error('Erreur:', error));
        });
    });

    document.querySelectorAll('.btn-toggle-favorite').forEach(button => {
        const isFavorite = button.getAttribute('data-is-favorite') === 'true';
        if (isFavorite) {
            button.classList.add('star-filled');
            button.classList.remove('star-empty');
        } else {
            button.classList.add('star-empty');
            button.classList.remove('star-filled');
        }
    });

});
