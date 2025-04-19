document.addEventListener('DOMContentLoaded', function() {
    const typeSelect = document.getElementById('id_type');
    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');

        async function updateCategories() {
        const typeId = typeSelect?.value;
        subcategorySelect.innerHTML = '<option value="">---------</option>'

        if (!typeId) {
            categorySelect.innerHTML = '<option value="">---------</option>';
            return;
        }

        try {
            const response = await fetch(`/admin/get_categories/?type__id__exact=${typeId}`);
            const categories = await response.json();

            categorySelect.innerHTML = '<option value="">---------</option>';
            categories.forEach(cat => {
                categorySelect.add(new Option(cat.name, cat.id));
            });
        } catch (error) {
            console.error('Error fetching categories:', error);
        }
    }

    async function updateSubcategories() {
        const categoryId = categorySelect?.value;
        if (!categoryId) {
            subcategorySelect.innerHTML = '<option value="">---------</option>';
            return;
        }

        try {
            const response = await fetch(`/admin/get_subcategories/?category__id__exact=${categoryId}`);
            const subcategories = await response.json();

            subcategorySelect.innerHTML = '<option value="">---------</option>';
            subcategories.forEach(subcat => {
                subcategorySelect.add(new Option(subcat.name, subcat.id));
            });
        } catch (error) {
            console.error('Error fetching categories:', error);
        }
    }

    if (typeSelect) {
        typeSelect.addEventListener('change', updateCategories);
    }
    if (categorySelect) {
        categorySelect.addEventListener('change', updateSubcategories);
    }

    if (typeSelect?.value) {
        updateCategories();
    }if (categorySelect?.value) {
        updateSubcategories();
    }
});