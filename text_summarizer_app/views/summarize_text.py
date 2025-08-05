from django.views.decorators.csrf import csrf_exempt
from ..services import summarize_with_groq
from django.shortcuts import render


@csrf_exempt
def summarize_text(request):
    if request.method == "POST":
        try:
            text = request.POST.get("text", "").strip()
            tone = request.POST.get("tone", "").strip().lower()
            length = request.POST.get("length", "").strip().lower()

            if not text or len(text) < 20:
                return render(
                    request,
                    "../website/summarize_text.html",
                    {"error": "Text is required and should be at least 20 characters."},
                )

            if not tone:
                return render(
                    request,
                    "website/summarize_text.html",
                    {"message": "Tone is required"},
                )

            if not length:
                return render(
                    request,
                    "website/summarize_text.html",
                    {"message": "Length is required"},
                )

            summary = summarize_with_groq(text, tone, length)
            if summary.startswith("Error:"):
                return render(
                    request, "website/summarize_text.html", {"error": summary}
                )

            return render(request, "website/summarize_text.html", {"summary": summary})

        except Exception as ex:
            return render(
                request,
                "website/summarize_text.html",
                {"message": "Something went wrong", "error": str(ex)},
            )

    return render(
        request, "website/summarize_text.html", {"message": "Method not allowed"}
    )
