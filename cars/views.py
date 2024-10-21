from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Car, Comment
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# СПИСОК АВТОМОБИЛЕЙ
class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars' # Задаём имя для использования в шаблоне

# СВЕДЕНИЯ ОБ АВТОМОБИЛЕ
class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # получаем информацию об объекте
        context['comments'] = Comment.objects.filter(car=self.object) # создаём список comments и записываем туда результат запроса из таблицы comment
        return context

# СОЗДАНИЕ ОБЪЕКТА АВТОМОБИЛЬ
class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    template_name = 'cars/car_form.html'
    fields = ['make', 'model', 'year', 'description']
    success_url = reverse_lazy('car_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user # Устанавливаем текущего пользователя как владельца автомобиля
        return super().form_valid(form)

# РЕДАКТИРОВАНИЕ АВТОМОБИЛЯ
class CarUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Car
    template_name = 'cars/car_form.html'
    fields = ['make', 'model', 'year', 'description']
    success_url = reverse_lazy('car_list')

    # Проверяем, что текущий пользователь является владельцем автомобиля
    def test_func(self):
        car = self.get_object()
        return self.request.user == car.owner # Возвращаем True, если пользователь — владелец автомобиля

        # Добавляем информацию об автомобиле в контекст шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car'] = self.object
        return context

# УДАЛЕНИЕ АВТОМОБИЛЯ
class CarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Car
    template_name = 'cars/car_confirm_delete.html'
    success_url = reverse_lazy('car_list')

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.owner


# ДОБАВЛЕНИЕ КОММЕНТАРИЯ К АВТОМОБИЛЮ
class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        car = Car.objects.get(pk=pk) # Получаем автомобиль по id
        content = request.POST.get('content') # Получаем содержание комментария из POST-запроса
        if content: Comment.objects.create(car=car, author=request.user, content=content) # Создаем новый объект комментарий
        return redirect('car_detail', pk=pk)

# КНОПКА ВЫХОДА
class CustomLogoutView(views.LogoutView):
    next_page = 'car_list'

# РЕГИСТРАЦИЯ
def register(request):
    if request.method == 'POST': # Если это POST-запрос, обрабатываем данные формы
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт был создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm() # Если это GET-запрос, отображаем пустую форму
        return render(request, 'users/register.html', {'form': form}) # Рендерим страницу регистрации
