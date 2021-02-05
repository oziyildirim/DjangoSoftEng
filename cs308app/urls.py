from rest_framework.routers import DefaultRouter
from django.urls import path, include
from.import views
from.views import*


router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('product', ProductViewSet, basename='product')
router.register('order', OrderViewSet, basename='order')
router.register('orderitem', OrderItemViewSet, basename='orderitem')
router.register('basketitem', BasketItemViewSet, basename='basketitem')
router.register('comment', CommentsViewSet, basename='Comment')
router.register('category', CategoryViewSet, basename='category')
router.register('favourites', FavouritesViewSet, basename='favourites')
router.register('address', AddressViewSet, basename='address')
router.register('pho', PhotosViewSet, basename='photos')
router.register('comment', CommentsViewSet, basename='comments')
router.register('procat', ProcatViewSet, basename='procat')
router.register('orderaddresschange', OACViewSet, basename='OAC')


urlpatterns = [
    #path('', views.home, name='home'),
    path('', include(router.urls)),
    path('signup/', SignupViewSet.as_view()),                   #on readme
    path('login/', LoginViewSet.as_view()),                     #on readme
    path('forgot/', forgetMyPassword.as_view()),  
    path('forgotmobile/', forgotPasswordforMobile.as_view()), 
    path('myaddress/<int:id>/', myAddress.as_view()),
    # path('signup/<string:'username'>/', SignupViewSet.as_view())
    path('photos/', ProductphotosViewSet.as_view()),            #on readme
    path('prod/<int:id>/', productIncreaseViewed.as_view()),
    path('reccom/', recommendedProduct.as_view()),
    path('favs/<int:id>/', FavouriteList.as_view()),            #on readme
    path('pass/', ChangePassword.as_view()),                    #on readme
    path('changeuser/', ChangeUserInfo.as_view()),              #on readme
    path('search/', Searchlist.as_view()),                      #on readme
    path('emailconfirm/', EmailConfirmation.as_view()),         #on readme
    path('basket/<int:id>/', BasketUse.as_view()),              #on readme
    path('ord/', OrderUse.as_view()),                           #on readme
    path('ord/<int:id>/', getOrder.as_view()),                  #on readme
    path('orditem/<int:id>/',getOrderItem.as_view()),           #on readme
    path('categoryitems/<int:id>/',filt.as_view()),   #should be updated
    path('comments/<int:id>/',comments.as_view()),              #on readme
    path('categorynames/<int:id>',categoryNames.as_view()),     #on readme    
    path('commentapproval/',commentApproval.as_view()),         #on readme
    path('deneme/<int:id>/',deneme.as_view()),                  # test
    path('usercomments/<int:id>/',userComments.as_view()),      #on readme
    path('manage/<int:id>/',ProductManager.as_view()),          #on readme
    path('pdfsend/<int:id>/',pdfInvoice.as_view()),              #later
  	path('seepdf/<int:id>/',seeInvoicePdf.as_view()),           #later
    path('categorise/<int:id>/',addCategoryInfo.as_view()),     #on readme
    path('addphoto/',addPhoto.as_view()),                       #on readme
    path('status/',orderStatus.as_view()),                      #on readme
    path('ozan/<int:id>/',ozan.as_view()),                               # test
    path('oac/', orderaddresschange.as_view()),                 #on readme
    path('pay/', paymentSystem.as_view()),
    path('discountpanel/',discounts.as_view()),
    path('campaigns/',campaings.as_view()),
    path('cancelorder/<int:id>/',OrderCancelReq.as_view()),
    path('campaignitems/<int:id>/',campaingitems.as_view()),#on readme
    path('categorysales/',categorysales.as_view()),
    path('brandsales/',brandsales.as_view()),
    path('ml/<int:id>/',ML.as_view()),
    path('orderpage/',OrderPagination.as_view()),
    path('propage/',ProductPagination.as_view()),
    path('addresspage/',AddressPagination.as_view()),
    path('commentpage/',CommentPagination.as_view()),
    #path('product/', include(router))
]