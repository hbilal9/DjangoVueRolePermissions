import subprocess
from django.views.decorators.csrf import csrf_exempt
from core.settings import BASE_DIR
from django.http import JsonResponse

@csrf_exempt
def github_webhook(request):
    try:
        path = f'{BASE_DIR}/shell/pull_run.sh'
        subprocess.run(["bash", path])
        return JsonResponse({'message': 'proccess run successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)