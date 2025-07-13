// إعداد متغيرات المنتج (يمكنك تغيير productId حسب الحاجة)
const productId = 1; // مثال: عرض المنتج رقم 1
const apiBase = '/api';
let userToken = localStorage.getItem('access_token') || '';

// تحميل تفاصيل المنتج
async function loadProduct() {
    const res = await fetch(`${apiBase}/products/${productId}/`);
    const product = await res.json();
    document.getElementById('product-details').innerHTML = `
        <div class="row align-items-center">
            <div class="col-md-3 text-center mb-3 mb-md-0">
                <img src="${product.image || 'https://via.placeholder.com/180'}" class="product-img" alt="صورة المنتج">
            </div>
            <div class="col-md-9">
                <h2>${product.name}</h2>
                <p class="text-muted">${product.description}</p>
                <div class="mb-2">
                    <span class="fw-bold">السعر:</span> ${product.price} ريال
                </div>
                <div>
                    <span class="fw-bold">متوسط التقييم:</span> 
                    ${renderStars(product.average_rating)}
                    <span class="ms-2">(${product.total_reviews} مراجعة)</span>
                </div>
            </div>
        </div>
    `;
}

// تحميل المراجعات
async function loadReviews() {
    const stars = document.getElementById('filter-stars').value;
    const sort = document.getElementById('sort-reviews').value;
    let url = `${apiBase}/reviews/?product=${productId}&sort=${sort}`;
    if (stars) url += `&rating=${stars}`;
    const res = await fetch(url);
    const data = await res.json();
    const reviews = data.results || data; // دعم pagination أو قائمة مباشرة
    document.getElementById('reviews-list').innerHTML = reviews.length ? reviews.map(renderReview).join('') : '<div class="text-center text-muted">لا توجد مراجعات بعد.</div>';
}

// رسم نجوم التقييم
function renderStars(rating) {
    rating = Math.round(rating);
    let html = '';
    for (let i = 1; i <= 5; i++) {
        html += `<span class="star${i <= rating ? '' : ' gray'}">&#9733;</span>`;
    }
    return html;
}

// رسم مراجعة واحدة
function renderReview(review) {
    return `
    <div class="review-card">
        <div class="d-flex justify-content-between align-items-center mb-1">
            <span class="review-user">${review.user?.full_name || review.user?.username || 'مستخدم'}</span>
            <span class="review-meta">${renderStars(review.rating)} | ${review.created_at?.slice(0,10) || ''}</span>
        </div>
        <div class="mb-2">${review.content}</div>
        <div class="d-flex align-items-center review-meta mb-1">
            <span class="me-3">الإعجابات: <b>${review.helpful_votes}</b></span>
            <span class="me-3">عدم الإعجاب: <b>${review.unhelpful_votes}</b></span>
            <span class="me-3">المشاهدات: <b>${review.views_count || 0}</b></span>
            ${review.user_interaction ? `<span class="badge bg-success ms-2">تفاعلت</span>` : ''}
            ${review.has_user_reported ? `<span class="badge bg-danger ms-2">مبلغ عنها</span>` : ''}
        </div>
        <div class="review-actions">
            <button class="btn btn-outline-success btn-sm${review.user_interaction==='helpful' ? ' active' : ''}" onclick="voteReview(${review.id}, 'helpful')">إعجاب</button>
            <button class="btn btn-outline-danger btn-sm${review.user_interaction==='unhelpful' ? ' active' : ''}" onclick="voteReview(${review.id}, 'unhelpful')">عدم إعجاب</button>
            <button class="btn btn-outline-warning btn-sm" onclick="reportReview(${review.id})">إبلاغ</button>
        </div>
    </div>
    `;
}

// التصويت على مراجعة
async function voteReview(reviewId, type) {
    if (!userToken) return alert('يجب تسجيل الدخول للتفاعل.');
    await fetch(`${apiBase}/review-interactions/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${userToken}`
        },
        body: JSON.stringify({ review_id: reviewId, interaction_type: type })
    });
    loadReviews();
}

// الإبلاغ عن مراجعة
async function reportReview(reviewId) {
    if (!userToken) return alert('يجب تسجيل الدخول للإبلاغ.');
    const reason = prompt('سبب الإبلاغ (مثلاً: محتوى غير مناسب):');
    if (!reason) return;
    await fetch(`${apiBase}/review-reports/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${userToken}`
        },
        body: JSON.stringify({ review_id: reviewId, reason: 'inappropriate', description: reason })
    });
    alert('تم إرسال البلاغ!');
    loadReviews();
}

// إرسال مراجعة جديدة
const reviewForm = document.getElementById('review-form');
if (reviewForm) {
    reviewForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        if (!userToken) return alert('يجب تسجيل الدخول لإرسال مراجعة.');
        const rating = document.getElementById('review-rating').value;
        const content = document.getElementById('review-content').value;
        await fetch(`${apiBase}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken}`
            },
            body: JSON.stringify({ product_id: productId, rating, title: 'مراجعة من الواجهة', content })
        });
        document.getElementById('review-content').value = '';
        document.getElementById('review-rating').value = '';
        document.querySelector('#addReviewModal .btn-close').click();
        loadReviews();
    });
}

// نجوم التقييم في النموذج
const starRatingDiv = document.getElementById('star-rating');
if (starRatingDiv) {
    for (let i = 1; i <= 5; i++) {
        const star = document.createElement('span');
        star.className = 'star gray';
        star.innerHTML = '&#9733;';
        star.onclick = function() {
            document.getElementById('review-rating').value = i;
            Array.from(starRatingDiv.children).forEach((s, idx) => {
                s.className = 'star' + (idx < i ? '' : ' gray');
            });
        };
        starRatingDiv.appendChild(star);
    }
}

// تحميل البيانات عند تغيير الفلاتر
['filter-stars', 'sort-reviews'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', loadReviews);
});

// تحميل البيانات عند بدء الصفحة
loadProduct();
loadReviews(); 