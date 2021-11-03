from django.shortcuts import render, redirect
from .models import Document, Chapter, Section
from django.contrib.auth.decorators import login_required
from account.models import CustomUser


@login_required
def index(request):
    uname = str(request.user)
    request.session['user_name'] = uname
    user = CustomUser.objects.get(user_name=uname)

    documents = Document.objects.filter(owner=user)

    if request.method == "POST":
        file_name = request.POST.get('file_name')
        d = Document(owner=user, title=file_name)
        d.save()
        return redirect("editor_view", file_id=d.document_id)
    return render(request, 'index.html', {"documents": documents, "user_name": uname})


@login_required
def editor_view(request, file_id):
    doc = Document.objects.get(document_id=file_id)

    if Chapter.objects.filter(document=doc).exists():
        chapters = Chapter.objects.filter(document=doc)
        sections = {}
        for chapter in chapters:
            sec = Section.objects.filter(chapter=chapter)
            sections[chapter] = sec

        context = {'document': doc, 'chapters': chapters, 'sections': sections}
    else:
        context = {'document': doc}
    return render(request, 'editor_view.html', context)


@login_required
def section_view(request, file_id, chapter_slug, section_slug):
    doc = Document.objects.get(document_id=file_id)
    chapter = Chapter.objects.get(document=doc, slug=chapter_slug)
    section = Section.objects.get(chapter=chapter, slug=section_slug)

    if request.method == "POST":
        section_title = request.POST.get('section_name')
        if Section.objects.filter(chapter=chapter, title=section_title).exists():
            section.content = request.POST.get('content')
            section.save()
        else:
            section.title = request.POST.get('section_name')
            section.content = request.POST.get('content')
            section.save()

            return redirect("section_view", file_id=file_id,
                            chapter_slug=chapter_slug, section_slug=section.slug)

    context = {'chapter': chapter, 'section': section}
    return render(request, 'section_view.html', context)


@login_required
def chapter_view(request, file_id, slug):
    doc = Document.objects.get(document_id=file_id)
    chapter = Chapter.objects.get(document=doc, slug=slug)

    if request.method == "POST":
        chapter_title = request.POST.get('chapter_name')
        if Chapter.objects.filter(document=doc, title=chapter_title).exists():
            chapter.description = request.POST.get('content')
            chapter.save()
        else:
            chapter.title = request.POST.get('chapter_name')
            chapter.description = request.POST.get('content')
            chapter.save()

            return redirect("chapter_view", file_id=file_id, slug=chapter.slug)

    context = {'chapter': chapter}

    return render(request, 'chapter_view.html', context)


@login_required
def new_chapter_view(request, file_id):
    doc = Document.objects.get(document_id=file_id)

    if request.method == "POST":
        chapter_title = request.POST.get('chapter_name')
        chapter_content = request.POST.get('content')

        if Chapter.objects.filter(document=doc, title=chapter_title).exists():
            print("Already exists")
        else:
            chapter = Chapter(
                document=doc, title=chapter_title, description=chapter_content)
            chapter.save()
            return redirect("chapter_view", file_id=file_id, slug=chapter.slug)

    return render(request, 'chapter_view.html')


@login_required
def new_section_view(request, file_id, chapter_slug):
    doc = Document.objects.get(document_id=file_id)
    chapter = Chapter.objects.get(document=doc, slug=chapter_slug)

    if request.method == "POST":
        section_title = request.POST.get('section_name')
        section_content = request.POST.get('content')

        if Section.objects.filter(chapter=chapter, title=section_title).exists():
            print("Already exists")
        else:
            section = Section(
                chapter=chapter, title=section_title, content=section_content)
            section.save()
            return redirect("section_view", file_id=file_id,
                            chapter_slug=chapter_slug, section_slug=section.slug)

    return render(request, 'section_view.html')
