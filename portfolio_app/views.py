from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import ProjectForm, PortfolioForm
from django.shortcuts import get_object_or_404
from django.contrib import messages

def index(request):
    student_active_portfolios = Student.objects.select_related('portfolio').all().filter(portfolio__is_active=True)
    print("active portfolio query set", student_active_portfolios)
    return render( request, 'portfolio_app/index.html', {'student_active_portfolios':student_active_portfolios})

def createProject(request, portfolio_id):
    form = ProjectForm()
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    
    if request.method == 'POST':
        # Create a new dictionary with form data and portfolio_id
        project_data = request.POST.copy()
        project_data['portfolio_id'] = portfolio_id
        
        form = ProjectForm(project_data)
        if form.is_valid():
            # Save the form without committing to the database
            project = form.save(commit=False)
            # Set the portfolio relationship
            project.portfolio = portfolio
            project.save()

            # Redirect back to the portfolio detail page
            return redirect('portfolio-detail', portfolio_id)

    context = {'form': form}
    return render(request, 'portfolio_app/project_form.html', context)

def updateProject(request, pk):
  project = get_object_or_404(Project, pk=pk)

  if request.method == 'POST':
    form = ProjectForm(request.POST, instance = project)
    if form.is_valid():
      form.save()
      return redirect('project-detail', pk=pk)
  else:
    form = ProjectForm(instance=project)
    context={
     'form': form,
     'project': project,
    }
  return render(request, 'portfolio_app/project_update.html', context)

def updatePortfolio(request, pk):
  portfolio = get_object_or_404(Portfolio, pk=pk)
  
  if request.method == 'POST':
    form = PortfolioForm(request.POST, instance = portfolio)
    if form.is_valid():
      form.save()
      return redirect('portfolio-detail', pk=pk)
  else:
    form = PortfolioForm(instance=portfolio)
    context={
     'form': form,
     'portfolio': portfolio,
    }
  return render(request, 'portfolio_app/portfolio_update.html', context)

def deleteProject(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        # Redirect back to the portfolio detail page
        return redirect('portfolio-detail', pk=project.portfolio.id)

    context = {'project': project}
    return render(request, 'portfolio_app/project_delete.html', context)

# Create your views here.
class StudentListView(generic.ListView):
    model = Student
class StudentDetailView(generic.DetailView):
    model = Student

class PortfolioListView(generic.ListView):
    model = Portfolio
class PortfolioDetailView(generic.DetailView):
    model = Portfolio   
    def get_context_data(self, **kwargs):
        context = super(PortfolioDetailView, self).get_context_data(**kwargs)
        project_list = Project.objects.filter(portfolio_id=self.object)
        context['project_list'] = project_list
        return context 

class ProjectListView(generic.ListView):
    model = Project
class ProjectDetailView(generic.DetailView):
    model = Project       