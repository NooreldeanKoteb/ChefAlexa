from django.shortcuts import render
from django.http import JsonResponse
from .forms import homeForm,userForm
from .models import user
# from .models import home


def userInfo(request):
    users = {}
    for userVal in user.objects.all():
        users[str(userVal.email)] = [userVal.name, userVal.allergies, userVal.Kosher, userVal.Vegan, userVal.Vegetarian, userVal.Diabetic,
                                  userVal.Gluten_Free, userVal.Lactose_Intolerant, userVal.QuicknEazy, userVal.SlowCooker,
                                  userVal.BBQnGrill, userVal.American, userVal.Southern, userVal.Asian, userVal.Thai, userVal.Chinese,
                                  userVal.Indian, userVal.Mexican, userVal.Italian, userVal.European]
    return JsonResponse(users)


def welcomePage(request):
    form = homeForm()

    if request.method == "POST":
        form = homeForm(request.POST)

        if form.is_valid():
            return formPost(request)
        else:
            print('invalid form')
    return render(request, 'index.html', {'form': form})


def profile(request):
    return render(request, 'profile.html')


def formPost(request):
    form = userForm()

    if request.method == "POST":
        form = userForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
        else:
            print('invalid form')

    return render(request, 'userForm.html', {'form': form})
