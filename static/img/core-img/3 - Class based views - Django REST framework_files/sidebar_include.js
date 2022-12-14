var include = '';



include += '<a href="https://dev.hel.fi">';
include += '<img width="130px" src="https://fund-rest-framework.s3.amazonaws.com/helsinki-logo-drf.png"></img>';
include += '</a>';


include += '<p><a class="promo" href="https://dev.hel.fi">City of Helsinki Open Software Development</a></p>';



include += '<p><a href="https://fund.django-rest-framework.org/topics/funding/">Fund Django REST framework</a></p>'

document.getElementById('sidebarInclude').innerHTML = include;
