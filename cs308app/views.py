from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
import random
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, generics, mixins, static, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter, BaseFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render
from .models import *
from.serializers import *
from django.db.models import Q
#from rest_framework.pagination import PageNumberPagination
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
# Create your views here.


# ML icin reserve

class ML(APIView):

    def get(self,request,id):
        try:
            arr={"Accesories":0,"Clothing":0,"Technology":0}
            onat = Order.objects.filter(user=id)
            for onatcik in onat:
                seray=OrderItem.objects.filter(order=onatcik.order_id)
                for seraycik in seray:
                    try:
                        quantity=seraycik.quantity
                        ceyda=seraycik.product
                        ozan=ProductCategory.objects.get(product=ceyda.product_id)
                        beste=Category.objects.get(category_id=ozan.category.category_id)
                        arr[beste.category_name]+=quantity
                    except:
                        pass
            max = 0
            key = ""
            for i in arr:
                if arr.get(i) > max:
                    max = arr.get(i)
                    key = i
            berrin = Category.objects.get(category_name=key)
            ilgin = ProductCategory.objects.filter(category=berrin.category_id)
            proarr = []
            for ilgincik in ilgin:
                if ilgincik.product.rating >= 4:
                    serializer = ProductSerializer(ilgincik.product)
                    proarr.append(serializer.data)
            return Response(proarr[:3],status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

###################################################


class SignupViewSet(APIView):

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                seray = User.objects.filter(email=request.data["email"])
                for seraycik in seray:
                    return Response({"message": "email exists"}, status=status.HTTP_400_BAD_REQUEST)
                print(serializer.validated_data)
                verification_code = str(random.randint(100000, 999999))
                serializer.validated_data["verification_code"] = verification_code
                serializer.save()
                seray1 = User.objects.get(email=request.data["email"])
                template = render_to_string('email_template.txt', {
                                            'name': serializer.data['first_name'], 'code': verification_code, 'link': '127.0.0.1:3000/emailconfirmation/%d' % seray1.user_id})
                email = EmailMessage(
                    'Verification for Greentings',
                    template,
                    settings.EMAIL_HOST_USER,
                    [serializer.data['email']],
                )

                email.fail_silently = False
                email.send()

                ser = LoginSerializer(serializer.data)
                return Response(ser.data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Wrong JSON format."}, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(APIView):

    def post(self, request):

        try:
            seray = User.objects.get(email=request.data["email"])
            if seray.password == request.data["password"]:
                serializer = LoginSerializer(seray)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response({"message": "password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "email does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"Wrong JSON format."}, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    def post(self, request):
        try:
            seray = User.objects.get(user_id=request.data["user_id"])
            if seray.password == request.data["old_password"]:
                seray.password = request.data["new_password"]
                seray.save()
                ser = LoginSerializer(seray)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Old password does not match."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Wrong JSON format."}, status=status.HTTP_400_BAD_REQUEST)


class forgetMyPassword(APIView):
    def post(self,request):
        try:
            seray = User.objects.get(email=request.data["email"])

            verification_code = str(random.randint(100000, 999999))

            seray.verification_code = verification_code
            seray.save()

            template = render_to_string('forgot_my_password.txt', {
                                                'name': seray.first_name, 'link': '127.0.0.1:3000/forgotconfirmation/%d' % seray.user_id,'code':verification_code})
            email = EmailMessage(
                'Forgot my Password on Greentings',
                template,
                settings.EMAIL_HOST_USER,
                [seray.email],
            )

            email.fail_silently = False
            email.send()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        try:
            seray = User.objects.get(user_id=request.data["user_id"])
            if seray.verification_code == request.data["verification_code"]:
                seray.password = request.data["password"]
                seray.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'message':'Wrong code.'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class forgotPasswordforMobile(APIView):

    def post(self,request):
        try:
            seray = User.objects.get(email=request.data["email"])

            verification_code = str(random.randint(100000, 999999))

            seray.verification_code = verification_code
            seray.save()

            template = render_to_string('forgot_for_mobile.txt', {
                                                'name': seray.first_name,'code':verification_code})
            email = EmailMessage(
                'Forgot my Password on Greentings',
                template,
                settings.EMAIL_HOST_USER,
                [seray.email],
            )

            email.fail_silently = False
            email.send()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            seray = User.objects.get(email=request.data["email"])
            if seray.verification_code == request.data["verification_code"]:
                seray.password = request.data["password"]
                seray.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'message':'Wrong code.'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangeUserInfo(APIView):
    
    def post(self, request):
        try:
            seray = User.objects.get(user_id=request.data["user_id"])
            seray.first_name = request.data["first_name"]
            seray.last_name = request.data["last_name"]
            seray.phone_number = request.data["phone_number"]
            seray2 = User.objects.filter(email=request.data["email"])
            for seray2cik in seray2:
                if seray2cik.user_id != seray.user_id:
                    return Response({"message": "Email exists for another account."}, status=status.HTTP_400_BAD_REQUEST)
                seray.save()
                ser = LoginSerializer(seray)
                return Response(ser.data, status=status.HTTP_200_OK)
            seray.email = request.data["email"]
            seray.save()
            ser = LoginSerializer(seray)
            return Response(ser.data, status=status.HTTP_200_OK)
        except:
            return Response({"message":"Wrong JSON format."}, status=status.HTTP_400_BAD_REQUEST)


class myAddress(APIView):
    def get(self,request,id):
        try:
            ceyda = Address.objects.filter(user=id)
            arr = []
            for ceydacik in ceyda:
                serializer = AddressSerializer(ceydacik)
                arr.append(serializer.data)
            return Response(arr,status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class pdfInvoice(APIView):
    def get(self, request, id):
        try:
            orderinfo = Order.objects.get(order_id=id)
            orderuser = User.objects.get(user_id=str(orderinfo.user))
            orderitems = OrderItem.objects.filter(order=id)
            name = "invoice_number_"+str(id)+".pdf"
            c = canvas.Canvas("invoice_number_"+str(id)+".pdf")
            c.setPageSize((2600, 3050))
            c.drawInlineImage(
                "https://sucourse.sabanciuniv.edu/plus/pluginfile.php/1/theme_lambda/logo/1606258893/sabanci_universitesi_logo_rgb.jpg", 0, 3050-331, 769, 331)
            c.drawInlineImage(
                "https://i.ibb.co/DfL1J4V/Greentings-3dots-whiteback.jpg", 2600-512, 3050-120, 512, 120)
            c.setFont('Arial', 80)
            text = "INVOICE"
            c.drawString(1000, 2700, text)
            c.setFont('Arial', 45)
            text2 = "Issued by: Greentings"
            c.drawString(180, 2500, text2)
            text3 = "Issued to: " + \
                str(orderuser.first_name)+" "+str(orderuser.last_name)
            c.drawString(180, 2420, text3)
            text4 = "Invoice number: "+str(id)
            c.drawString(180, 2340, text4)
            text5 = "Invoice date: " + str(orderinfo.date)
            c.drawString(180, 2260, text5)

            text22 = "Description"
            c.drawString(100, 1800, text22)
            text23 = "Price"
            c.drawString(1900, 1800, text23)
            text24 = "Quantity"
            c.drawString(2100, 1800, text24)
            y = 1800
            for orderitem in orderitems:
                y = y-80
                item = Product.objects.get(product_id=str(orderitem.product))
                text7 = str(item.product_name)
                c.drawString(100, y, text7)
                text8 = str(item.price)
                c.drawString(1900, y, text8)
                text9 = str(orderitem.quantity)
                c.drawString(2100, y, text9)
            y = y-100
            text10 = "Total price: " + str(orderinfo.total_price)
            c.drawString(2000, y, text10)

            c.save()
            template = render_to_string('invoice.txt', {
                'name': orderuser.first_name, 'order_id': orderinfo.order_id})
            email = EmailMessage(
                'PDF Invoice',
                template,
                settings.EMAIL_HOST_USER,
                [orderuser.email],
            )
            email.attach_file(name)
            email.fail_silently = False
            email.send()
            return Response({"message": "oldu"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "püü sana"}, status=status.HTTP_400_BAD_REQUEST)


class seeInvoicesInfo(APIView):
    def get(self, request):
        try:
            orders = Order.objects.all()
            arr = []
            for order in orders:
                user = User.objects.get(user_id=str(order.user))
                output = {
                    "order_id": order.order_id,
                    "name": user.first_name,
                    "surname": user.last_name,
                    "email": user.email,
                    "date": order.date
                }
                arr.append(output)
            return Response(arr, status=status.HTTP_200_OK)
        except:
            return Response({"message": "no invoice"}, status=status.HTTP_400_BAD_REQUEST)


class seeInvoicePdf(APIView):
    def get(self, request, id):
        try:
            orderinfo = Order.objects.get(order_id=id)
            orderuser = User.objects.get(user_id=str(orderinfo.user))
            orderitems = OrderItem.objects.filter(order=id)
            name = "invoice_number_" + str(id) + ".pdf"
            c = canvas.Canvas("invoice_number_" + str(id) + ".pdf")
            c.setPageSize((2600, 3050))
            c.drawInlineImage(
                "https://sucourse.sabanciuniv.edu/plus/pluginfile.php/1/theme_lambda/logo/1606258893/sabanci_universitesi_logo_rgb.jpg",
                0, 3050 - 331, 769, 331)
            c.drawInlineImage(
                "https://i.ibb.co/DfL1J4V/Greentings-3dots-whiteback.jpg", 2600 - 512, 3050 - 120, 512, 120)
            c.setFont('Arial', 80)
            text = "INVOICE"
            c.drawString(1000, 2700, text)
            c.setFont('Arial', 45)
            text2 = "Issued by: Greentings"
            c.drawString(180, 2500, text2)
            text3 = "Issued to: " + \
                    str(orderuser.first_name) + " " + str(orderuser.last_name)
            c.drawString(180, 2420, text3)
            text4 = "Invoice number: " + str(id)
            c.drawString(180, 2340, text4)
            text5 = "Invoice date: " + str(orderinfo.date)
            c.drawString(180, 2260, text5)

            text22 = "Description"
            c.drawString(100, 1800, text22)
            text23 = "Price"
            c.drawString(1900, 1800, text23)
            text24 = "Quantity"
            c.drawString(2100, 1800, text24)
            y = 1800
            for orderitem in orderitems:
                y = y - 80
                item = Product.objects.get(product_id=str(orderitem.product))
                text7 = str(item.product_name)
                c.drawString(100, y, text7)
                text8 = str(item.price)
                c.drawString(1900, y, text8)
                text9 = str(orderitem.quantity)
                c.drawString(2100, y, text9)
            y = y - 100
            text10 = "Total price: " + str(orderinfo.total_price)
            c.drawString(2000, y, text10)

            c.save()
            return Response({"message": "oldu"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "püü sana"}, status=status.HTTP_400_BAD_REQUEST)


class OrderCancelReq(APIView):
    def get(self,request,id):
        try:
            seray=OrderCancel.objects.all()
            arr=[]
            for seraycik in seray:
                serializer=OrderCancelSerializer(seraycik)
                dic = serializer.data
                dic["user_id"] = seraycik.order.user.user_id
                arr.append(dic)
            return Response(arr, status=status.HTTP_200_OK)
        except:
            return Response( status=status.HTTP_400_BAD_REQUEST)

    def post(self,request,id):
        try:
            seray=OrderCancel.objects.get(ordercancel_id=id)
            ceyda=OrderItem.objects.filter(order=seray.order.order_id)
            for ceydacik in ceyda:
                ceydacik.status=3
                ceydacik.save()
            
            template = render_to_string('ordercancelmail.txt', {
                                                'name': seray.order.user.first_name, 'orderid': seray.order.order_id})
            email = EmailMessage(
                'Order Cancellation on Greentings',
                template,
                settings.EMAIL_HOST_USER,
                [seray.order.user.email],
            )

            email.fail_silently = False
            email.send()

            seray.order.cancelled=True
            seray.order.save()
            seray.delete()

            return Response( status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,id):
        try:
            dict={}
            dict["order"]=id
            serializer=OrderCancelSerializer(data=dict)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        try:
            seray = OrderCancel.objects.get(ordercancel_id=id)
            seray.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class recommendedProduct(APIView):
    def get(self,request):
        try:
            seray = Product.objects.filter(recommended=True)

            arr = []
            for seraycik in seray:
                serializer = ProductSerializer(seraycik)
                arr.append(serializer.data)
            return Response(arr,status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class productIncreaseViewed(APIView):
    def get(self,request,id):
        try:
            ceyda = Product.objects.get(product_id=id)
            ceyda.viewed = ceyda.viewed + 1
            ceyda.save()
            ser = ProductSerializer(ceyda)
            return Response(ser.data,status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,id):
        try:
            ceyda = Product.objects.get(product_id=id)
            ser = ProductSerializer(ceyda, request.data)
            ser.save()
            return Response(ser.data,status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductphotosViewSet(APIView):
    def post(self, request):
        try:
            seray = Photos.objects.filter(
                product_id=request.data["product_id"])
            arr = []
            for seraycik in seray:
                output = {
                    "image_id":seraycik.photos_id,
                    "image_url": seraycik.image_url
                }
                arr.append(output)
            return Response(arr, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({"message": "Wrong JSON format."}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        try:
            seray = Photos.objects.get(photos_id=request.data["id"])
            seray.delete()
            return Response( status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#class pagination(ListAPIView):


class campaings(APIView):
    def get(self,request):
        try:
            beste=CampaignInfo.objects.all()
            arr=[]
            for bestecik in beste:

                dict={}
                dict["campaign_id"]=bestecik.campaing_id
                dict["name"]=bestecik.name
                dict["description"]=bestecik.description
                dict["discount_rate"]=bestecik.discount_rate

                arr2=[]
                ceyda=Campaignitems.objects.filter(campaigninfo=bestecik.campaing_id)
                for ceydacik in ceyda:
                    arr2.append(ceydacik.product.product_id)
                dict["products"]=arr2
                arr.append(dict)
            return Response(arr,status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class discounts(APIView):
    def get(self,request):
        try:
            seray=CampaignInfo.objects.get(name=request.data["campaign_name"])
            ceyda=Campaignitems.objects.filter(campaigninfo=seray.campaing_id)
            arr = []
            for ceydacik in ceyda:
                serializer=ProductSerializer(ceydacik.product)
                arr.append(serializer.data)

            return Response(arr,status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def post(self,request):
        try:
            dict = {}
            dict["name"]=request.data["campaign"]
            dict["description"]=request.data["description"]
            dict["discount_rate"]=request.data["discount"]
            serializer = CampaignInfoSerializer(data=dict)
            if serializer.is_valid():
                serializer.save()
            arr=request.data["products"]
            for product in arr:
                seray= Product.objects.get(product_id=product)
                seray.price=seray.base_price*(1-request.data["discount"]/100)
                seray.discount=True
                seray.save()
                dict2={}
                dict2["product"]=product
                beste=CampaignInfo.objects.get(name=request.data["campaign"])
                dict2["campaigninfo"]=beste.campaing_id

                serializer2=CampaignitemsSerializer(data=dict2)
                if serializer2.is_valid():

                    serializer2.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        try:
            seray = CampaignInfo.objects.get(name=request.data["campaign_name"])
            ceyda = Campaignitems.objects.filter(campaigninfo=seray.campaing_id)
            for ceydacik in ceyda:
                # beste=Product.objects.get(product_id=ceydacik.product)
                beste = Product.objects.get(product_id=ceydacik.product.product_id)
                beste.price = beste.base_price
                beste.discount = False
                beste.save()
                ceydacik.delete()
            seray.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class categorysales(APIView):
    def get(self,request):
        try:
            #arr={"Accesories":0,"Clothing":0,"Technology":0}
            arr={}
            onat=Category.objects.all()
            for onatcik in onat:
                arr[onatcik.category_name]=0
            seray=OrderItem.objects.all()
            for seraycik in seray:
                try:
                    quantity=seraycik.quantity
                    ceyda=seraycik.product
                    ozan=ProductCategory.objects.get(product=ceyda.product_id)
                    beste=Category.objects.get(category_id=ozan.category.category_id)
                    arr[beste.category_name]+=quantity
                except:
                    pass
            print(arr)
            return Response(arr,status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class brandsales(APIView):
    def get(self,request):
        try:
            #arr={"WWF":0,"Bey Store":0,"Elvis & Kresse":0,"Gomi":0,"COUPER -ET- COUDRE":0,"EOE-Eye Wear":0,"Lula Mena":0,"Official Rebrand":0,"Reflect Studio":0}
            arr={}
            onat=Product.objects.all()
            for onatcik in onat:
                arr[onatcik.brand_name]=0
            seray = OrderItem.objects.all()
            for seraycik in seray:
                try:
                    quantity = seraycik.quantity
                    ceyda = seraycik.product
                    arr[ceyda.brand_name] += quantity
                except:
                    pass
            print(arr)
            return Response(arr, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class campaingitems(APIView):
    def post(self,request,id):
        try:
            seray=CampaignInfo.objects.get(campaing_id=id)
            ceyda=Campaignitems.objects.filter(campaigninfo=id)
            arr=[]
            for ceydacik in ceyda:
                beste=Product.objects.get(product_id=ceydacik.product.product_id)
                serializer=ProductSerializer(beste)
                arr.append(serializer.data)
            return Response(arr,status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FavouriteList(APIView):
    def get(self, request, id):
        try:
            seray = Favourites.objects.filter(
                user_id=id)
            arr = []
            for seraycik in seray:
                s = ProductSerializer(seraycik.product)
                arr.append(s.data)
            return Response(arr, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        try:
            seray = Favourites.objects.filter(user_id=id)
            for seraycik in seray:
                if str(seraycik.product) == str(request.data["product"]):
                    return Response({"message": "already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            request.data["user"] = id
            serializer = FavouritesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        seray = Favourites.objects.filter(user_id=id)
        for seraycik in seray:
            if str(seraycik.product) == request.data["product"]:
                seraycik.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ozan(APIView):
    def post(self, request,id):
        dic = request.data
        dic["user"] = id
        dic["rating"] = 1
        dic["recommended"] = False
        dic["real_stock"] = dic["stock"]
        dic["viewed"] = 0
        dic["base_price"] = dic["price"]
        dic["discount"] = False
        serializer = ProductSerializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            beste = Category.objects.get(category_name=request.data["category_name"]).category_id
            new_dic = {"product": serializer.data["product_id"], "category": beste}
            ser = ProductCategorySerializer(data=new_dic)
            if ser.is_valid():
                ser.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
       

class EmailConfirmation(APIView):
    def post(self, request):
        try:
            seray = User.objects.get(user_id=request.data["user_id"])
            verification_code = request.data["verification_code"]
            if seray.verification_code == verification_code:
                seray.verified = True
                seray.save()
                return Response({"message": "Verification codes match"}, status=status.HTTP_200_OK)
            return Response({"message": "Verification codes do not match"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Wrong JSON format."}, status=status.HTTP_400_BAD_REQUEST)


class BasketUse(APIView):
    def get(self, request, id):
        try:
            seray = BasketItem.objects.filter(
                user_id=id)
            arr = []
            for seraycik in seray:
                s = ProductSerializer(seraycik.product)
                d = s.data
                d["quantity"] = seraycik.quantity
                arr.append(d)
            return Response(arr, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        try:
            temp_id = id
            if id == 0:
                d = {'verified': False, 'user_exists':False}
                ozan = UserSerializer(data=d)
                if ozan.is_valid():
                    ozan.save()
                    temp_id = ozan.data["user_id"]
            arr = []
            onat = User.objects.get(user_id=temp_id)
            arr.append({'user_id': temp_id,'user_exists':onat.user_exists})
            ceyda = BasketItem.objects.filter(user_id=temp_id)
            for ceydacik in ceyda:
                if str(ceydacik.product) == str(request.data["product"]):
                    if ceydacik.product.stock >= (int(request.data["quantity"])-ceydacik.quantity):
                        red = int(request.data["quantity"]) - ceydacik.quantity
                        ceydacik.quantity = int(request.data["quantity"])
                        ceydacik.save()
                        ceydacik.product.stock -= red
                        ceydacik.product.save()
                        arr.append({"message": "quantity updated"})
                        return Response(arr, status=status.HTTP_200_OK)
                    else:
                        arr.append({"message": "stock is not enough"})
                        return Response(arr, status=status.HTTP_406_NOT_ACCEPTABLE)

            request.data["user"] = temp_id
            #request.data["quantity"] = 1
            serializer = BasketItemSerializer(data=request.data)
            if serializer.is_valid():
                pro = Product.objects.get(product_id=request.data["product"])
                if pro.stock >= 1:
                    pro.stock -= 1
                    pro.save()
                    serializer.save()
                    return Response(arr, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        seray = BasketItem.objects.filter(user_id=id)
        for seraycik in seray:
            if str(seraycik.product) == str(request.data["product"]):
                seraycik.product.stock += int(seraycik.quantity)
                seraycik.product.save()
                seraycik.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class OrderUse(APIView):
    def post(self, request):
        dic = request.data
        dic["total_price"] = 0
        serializer = OrderSerializer(data=dic)
        try:
            seray = BasketItem.objects.filter(user_id=request.data["user"])
            if len(seray) == 0:
                return Response({'message':'bos yapma hacim'}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
            
            tot_pri=0

            for seraycik in seray:
                dic = {}
                dic["quantity"] = seraycik.quantity
                dic["product"] = str(seraycik.product)
                dic["order"] = serializer.data["order_id"]
                tot_pri += seraycik.quantity*seraycik.product.price
                seraycik.product.real_stock -= int(seraycik.quantity)
                seraycik.product.save()
                ser = OrderItemSerializer(data=dic)
                if ser.is_valid():
                    ser.save()
                    seraycik.delete()
            
            ceyda = Order.objects.get(order_id=serializer.data["order_id"])
            ceyda.total_price = tot_pri
            ceyda.save()
            beste = OrderSerializer(ceyda)
            return Response(beste.data, status=status.HTTP_201_CREATED)

        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class getOrder(APIView):
    def get(self, request, id):
        seray = Order.objects.filter(user=id)
        arr = []
        try:
            for seraycik in seray:
                serializer = OrderSerializer(seraycik)
                arr.append(serializer.data)
            return Response(arr, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class getOrderItem(APIView):
    def get(self, request, id):
        try:
            seray = OrderItem.objects.filter(order=id)
            arr = []
            for seraycik in seray:
                ser = OrderItemStatusSerializer(seraycik)
                serializer = ProductSerializer(seraycik.product)
                data = serializer.data
                data["quantity"] = seraycik.quantity
                data["status"] = ser.data["status"]
                arr.append(data)
            return Response(arr, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class orderStatus(APIView):

    def post(self, request):
        try:
            seray = OrderItem.objects.get(
                order=request.data["order"], product=request.data["product"])
            seray.status = request.data["status"]
            seray.save()
            allDelivered = True
            items = []
            ilgin = OrderItem.objects.filter(order=request.data["order"])
            for ilgincik in ilgin:
                items.append(ilgincik)
                if ilgincik.status != 2:
                    allDelivered = False
            ceyda = Order.objects.get(order_id=request.data["order"])
            ceyda.allDelivered = allDelivered
            ceyda.save()
            serializer = OrderItemStatusSerializer(seray)

            arr = []
            for item in items:
                stats = ""
                if item.status == 0:
                    stats = "Getting Prepared"
                elif item.status == 1:
                    stats = "On Delivery"
                elif item.status == 2:
                    stats = "Delivered"
                else:
                    stats = "Cancelled"

                json = {'name':item.product.product_name,'brand':item.product.brand_name,'price':item.product.price,'quantity':item.quantity,'status':stats}
                arr.append(json)

            template = render_to_string('order_status.txt', {'name': seray.order.user.first_name,'items':arr, 'orderid':seray.order.order_id})
            email = EmailMessage(
                'Order on Greentings',
                template,
                settings.EMAIL_HOST_USER,
                [seray.order.user.email],
            )

            email.fail_silently = False
            email.send()



            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class paymentSystem(APIView):
    def post(self, request):
        # JSON {"credit_card_number": "", "cvv":"", "expiration_date":"", "name":""}
        try:
            ccn = request.data["credit_card_number"]
            cvv = request.data["cvv"]
            exp_date = request.data["expiration_date"]
            name = request.data["name"]
            return Response({"message": "Payment made."}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Missing info"}, status=status.HTTP_400_BAD_REQUEST)


class orderaddresschange(APIView):

    def get(self,request):
        try:
            onat = OrderAddressChange.objects.filter(verified=False)
            arr = []
            for onatcik in onat:
                ser = OrderAddressChangeSerializer(onatcik)
                arr.append(ser.data)
            return Response(arr, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self,request):
        try:
            dict = {}
            dict["order"] = request.data["order_id"]
            dict["address"] = request.data["address_id"]
            dict["verified"] = "False"
            serializer = OrderAddressChangeSerializer(data=dict)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self,request):
        try:
            beste=OrderAddressChange.objects.get(orderadresschange_id=request.data["oac_id"])
            beste.order.address=beste.address
            beste.order.save()
            beste.verified=True
            beste.save()

            template = render_to_string('address_change.txt', {
                                                'name': beste.order.user.first_name, 'orderid':beste.order.order_id})
            email = EmailMessage(
                'Address Changed on Order, Greentings',
                template,
                settings.EMAIL_HOST_USER,
                [beste.order.user.email],
            )

            email.fail_silently = False
            email.send()

            return Response( status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self,request):
        try:
            beste = OrderAddressChange.objects.get(orderadresschange_id=request.data["oac_id"])
            beste.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class comments(APIView):
    def get(self, request, id):
        buse = Comments.objects.filter(product=id, validation=True)
        arr = []
        try:
            for busecik in buse:
                serializer = CommentsSerializer(busecik)
                arr.append(serializer.data)
            return Response(arr, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        buse = Comments.objects.filter(product=id)
        totalpoint = 0
        size = 0
        for busecik in buse:
            size += 1
            serializer = CommentsSerializer(busecik)
            totalpoint += serializer.data["rating"]
        dic = {}
        dic["nickname"] = request.data["nickname"]
        dic["user_id"] = request.data["user_id"]
        dic["text"] = request.data["text"]
        dic["rating"] = request.data["rating"]
        dic["validation"] = request.data["validation"]
        dic["product"] = id
        print(dic)
        ser = CommentsSerializer(data=dic)
        try:
            if ser.is_valid():
                ser.save()
                ceyda = Product.objects.get(product_id=id)
                ceyda.rating = totalpoint/size
                ceyda.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response("error", status=status.HTTP_400_BAD_REQUEST)


class commentApproval(APIView):

    def get(self, request):
        buse = Comments.objects.filter(validation=False)
        arr = []
        try:
            for busecik in buse:
                serializer = CommentsSerializer(busecik)
                arr.append(serializer.data)
            return Response(arr, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        try:
            beste=request.data
            ceyda = Comments.objects.get(comment_id=beste)
            ceyda.validation=True
            ceyda.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        try:
            beste=request.data
            ceyda=Comments.objects.get(comment_id=beste)
            ceyda.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class userComments(APIView):
    def get(self,request,id):
        try:
            buse=Comments.objects.filter(user_id=id)
            print(buse)
            arr=[]
            for busecik in buse:
                print(busecik)
                serializer=CommentsSerializer(busecik)
                arr.append(serializer.data)
            return Response(arr,status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class categoryNames(APIView):
    def get(self, request, id):
        try:
            ceyda = ProductCategory.objects.filter(category=id)
            arr = []
            for ceydacik in ceyda:
                found = False
                data = Product.objects.get(product_id=str(ceydacik.product))
                if arr.count({"name": data.brand_name}):
                    found = True
                if found == False:
                    arr.append({"name": data.brand_name})
            return Response(arr, status=status.HTTP_200_OK)

        except:
            return Response("no product", status=status.HTTP_400_BAD_REQUEST)


class deneme(APIView):
    def post(self, request, id):
        ceyda = ProductCategory.objects.filter(category=id)
        arr = []
        if request.data["brand"] == "empty":
            try:
                for ceydacik in ceyda:
                    data = Product.objects.get(
                        product_id=str(ceydacik.product))
                    print(data.price)
                    if data.price >= int(request.data["price_lower"]) and data.price <= int(request.data["price_upper"]) and data.rating >= int(request.data["rating"]):
                        serializer = ProductSerializer(data)
                        arr.append(serializer.data)
                    else:
                        print("hello")
                return Response(arr, status=status.HTTP_202_ACCEPTED)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                for ceydacik in ceyda:
                    data = Product.objects.get(
                        product_id=str(ceydacik.product))
                    if data.price >= int(request.data["price_lower"]) and data.price <= int(request.data["price_upper"]) and data.rating >= int(request.data["rating"]) and data.brand_name == str(request.data["brand"]):
                        serializer = ProductSerializer(data)
                        arr.append(serializer.data)
                return Response(arr, status=status.HTTP_202_ACCEPTED)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class filt(APIView):
    def get(self,request,id):
        try:
            ceyda = ProductCategory.objects.filter(category=id)
            arr = []
            for ceydacik in ceyda:
                data = Product.objects.get(product_id=str(ceydacik.product))
                serializer = ProductSerializer(data)
                arr.append(serializer.data)

            return Response(arr, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self,request,id):
        ceyda = ProductCategory.objects.filter(category=id)
        arr = []
        if len(request.data["brand_name"]) == 0:
            try:
                for ceydacik in ceyda:
                    data = Product.objects.get(
                        product_id=str(ceydacik.product))
                    if data.price >= int(request.data["price_lower"]) and data.price <= int(request.data["price_upper"]) and data.rating >= int(request.data["rating"]):
                        serializer = ProductSerializer(data)
                        arr.append(serializer.data)
                return Response(arr, status=status.HTTP_202_ACCEPTED)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            for brand in request.data["brand_name"]:
                try:
                    for ceydacik in ceyda:
                        data = Product.objects.get(
                            product_id=str(ceydacik.product))
                        if data.price >= int(request.data["price_lower"]) and data.price <= int(request.data["price_upper"]) and data.rating >= int(request.data["rating"]) and data.brand_name == str(brand):
                            serializer = ProductSerializer(data)
                            arr.append(serializer.data) 
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(arr, status=status.HTTP_202_ACCEPTED)


class ProductManager(APIView):

    def get(self, request, id):
        ilgin = Product.objects.filter(user=id)
        arr = []
        try:
            for ilgincik in ilgin:
                serializer = ProductSerializer(ilgincik)
                arr.append(serializer.data)
            return Response(arr, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        try:
            dic = request.data
            dic["user"] = id
            dic["rating"] = 1
            dic["recommended"] = False
            dic["real_stock"] = dic["stock"]
            dic["viewed"] = 0
            dic["base_price"] = dic["price"]
            dic["discount"] = False
            serializer = ProductSerializer(data=dic)
            if serializer.is_valid():
                serializer.save()
                beste = Category.objects.get(
                    category_name=request.data["category_name"]).category_id
                new_dic = {
                    "product": serializer.data["product_id"], "category": beste}
                ser = ProductCategorySerializer(data=new_dic)
                if ser.is_valid():
                    ser.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            ilgin = Product.objects.get(product_id=request.data["product_id"])
            dic = request.data
            dic["user"] = id
            dic["rating"] = ilgin.rating
            dic["recommended"] = ilgin.recommended
            dic["discount"] = ilgin.discount
            dic["viewed"] = ilgin.viewed
            if request.data["price"] != ilgin.base_price:
                dic["base_price"] = request.data["price"]
                dic["price"] = (ilgin.price/ilgin.base_price) * request.data["price"]
            else:
                dic["base_price"] = ilgin.base_price
                dic["price"] = ilgin.price

            if request.data["stock"] != ilgin.real_stock:
                dic["real_stock"] = request.data["stock"]
                dic["stock"] -= ilgin.real_stock - ilgin.stock
            else:
                dic["real_stock"] = ilgin.real_stock
                dic["stock"] = ilgin.stock

            serializer = ProductSerializer(ilgin, data=dic)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            ilgin = Product.objects.get(product_id=request.data["product_id"])
            ilgin.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class addPhoto(APIView):
    def post(self, request):
        try:
            serializer = PhotosSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Wrong JSON format"}, status=status.HTTP_400_BAD_REQUEST)


class addCategoryInfo(APIView):

    def get(self, request, id):
        try:
            beste = ProductCategory.objects.filter(product=id)
            arr = []
            for bestecik in beste:
                arr.append({"category_name": bestecik.category.category_name})
            return Response(arr, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        try:
            beste = Category.objects.get(
                category_name=request.data["category_name"]).category_id
            if ProductCategory.objects.filter(category=beste, product=id):
                return Response({"message": "Already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            dic = {"category": beste, "product": id}
            serializer = ProductCategorySerializer(data=dic)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            seray = ProductCategory.objects.filter(product=id)
            count = 0
            for seraycik in seray:
                count += 1
            if count <= 1:
                return Response({"message": "Product must have at least one category."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            ilgin = Category.objects.get(
                category_name=request.data["category_name"]).category_id
            beste = ProductCategory.objects.filter(category=ilgin, product=id)
            for bestecik in beste:
                bestecik.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


# List Views with paginations


class Searchlist(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_name', 'description', 'brand_name')


class OrderPagination(ListAPIView):
    PageNumberPagination.page_size=10
    #queryset = Order.objects.all()
    filter_backends = (OrderingFilter,)
    serializer_class = OrderSerializer
    search_fields = ('date','total_price')
    pagination_class = PageNumberPagination

    
    def get_queryset(self,*args,**kwargs):
        queryset_list = Order.objects.all()
        query = self.request.GET.get('user')
        if query:
            queryset_list = queryset_list.filter(Q(user=query)).distinct()
        return queryset_list


class ProductPagination(ListAPIView):
    PageNumberPagination.page_size=10
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_name', 'description', 'brand_name')
    pagination_class = PageNumberPagination


class AddressPagination(ListAPIView):
    PageNumberPagination.page_size=10
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('city', 'state', 'address_line')
    pagination_class = PageNumberPagination


class CommentPagination(ListAPIView):
    PageNumberPagination.page_size=10
    #queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('rating', 'text', 'date','nickname')
    pagination_class = PageNumberPagination

    def get_queryset(self,*args,**kwargs):
        queryset_list = Comments.objects.filter(validation=True)              # validation true don
        query = self.request.GET.get('product')
        if query:
            queryset_list = queryset_list.filter(Q(product=query)).distinct()
        return queryset_list

# ModelViewSets Start from here. These are viewsets used on router, base url 127.0.0.1:8000.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class BasketItemViewSet(viewsets.ModelViewSet):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FavouritesViewSet(viewsets.ModelViewSet):
    queryset = Favourites.objects.all()
    serializer_class = FavouritesSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class PhotosViewSet(viewsets.ModelViewSet):
    queryset = Photos.objects.all()
    serializer_class = PhotosSerializer


class ProcatViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class OACViewSet(viewsets.ModelViewSet):
    queryset = OrderAddressChange.objects.all()
    serializer_class = OrderAddressChangeSerializer
