from asyncio.windows_events import NULL
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

def cadastro(request):
    """ Realiza o cadastro de uma pessoa no sistema. """
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'O campo nome nào pode ficar em branco!')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'O campo email nào pode ficar em branco!')
            return redirect('cadastro')
        if senhas_nao_sao_iguais(senha, senha2):
            messages.error(request, 'As senhas não são iguais!')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'E-mail de usuário já cadastrado!')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Nome de usuário já cadastrado!')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save
        messages.success(request, 'Usuário criado com sucesso')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    """ Realiza o Login do usuário no sistema, verificando dados. """
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos E-mail e Senha nào podem estar em branco!')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'E-mail ou senha incorretos!')
                return redirect('login')
        else:
            messages.error(request, 'E-mail ou senha incorretos!')
            return redirect('login')
    return render(request, 'usuarios/login.html')

def logout(request):
    """ Realiza o Logout do usuário. """
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    """ Verifica se  usuário está autenticado e o envia para o dashboard. """
    if request.user.is_authenticated:
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=request.user.id)

        dados = {
            'receitas' : receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def campo_vazio(campo):
    """ Verifica se o campo está vazio. """
    return not campo.strip()

def senhas_nao_sao_iguais(senha, senha2):
    """ Verifica se as senhas são iguais. """
    return  senha != senha2
