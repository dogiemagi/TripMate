import urllib.request
import urllib.parse
import json
import io
import sys
from PIL import Image

BASE = 'http://127.0.0.1:8000'
results = []

def test_endpoint(name, method, path, data=None, headers=None, is_json=True, is_multipart=False):
    url = BASE + path
    try:
        req_headers = headers or {}
        body = None
        if data is not None:
            if is_multipart:
                body = data
            elif is_json:
                body = json.dumps(data).encode('utf-8')
                req_headers['Content-Type'] = 'application/json'
            else:
                body = urllib.parse.urlencode(data).encode('utf-8')
                req_headers['Content-Type'] = 'application/x-www-form-urlencoded'
        
        req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            content = resp.read()
            parsed = None
            if resp.headers.get_content_type() == 'application/json':
                try:
                    parsed = json.loads(content.decode('utf-8'))
                except Exception:
                    pass
            print(f"[PASS] {name}: HTTP {status} (response size: {len(content)} bytes)")
            results.append((name, 'PASS', status, None))
            return True, parsed
    except Exception as e:
        code = getattr(e, 'code', 'ERR')
        print(f"[FAIL] {name}: HTTP {code} - {e}")
        results.append((name, 'FAIL', code, str(e)))
        return False, None

def run_all_tests():
    print("==================================================")
    print("       TripMate AI - Backend Test Suite           ")
    print("==================================================")
    
    test_endpoint('1. Health Check (/healthz)', 'GET', '/healthz')
    test_endpoint('2. Frontend Index HTML (/)', 'GET', '/')
    test_endpoint('3. Dedicated TripMate Chat Planner (/chat)', 'GET', '/chat')
    test_endpoint('4. OpenAPI Specs (/openapi.json)', 'GET', '/openapi.json')
    test_endpoint('5. Weather Forecast API', 'GET', '/api/v1/weather?city=Tokyo&days=3')
    test_endpoint('6. Itinerary Generator API', 'POST', '/api/v1/itinerary/generate', {
        'destination': 'Tokyo, Japan',
        'days': 2,
        'travel_style': 'Balanced',
        'pace': 'Moderate',
        'interests': ['Food', 'Sightseeing'],
        'budget_level': 'Moderate'
    })
    test_endpoint('7. Gastronomy Food Explore (POST)', 'POST', '/api/v1/food/explore', {
        'city': 'Tokyo',
        'dietary_preferences': ['Vegetarian']
    })
    test_endpoint('8. Gastronomy Food (GET)', 'GET', '/api/v1/food?city=Tokyo')
    test_endpoint('9. Budget Currency Convert API', 'POST', '/api/v1/budget/convert', {
        'from_currency': 'INR',
        'to_currency': 'USD',
        'amount': 5000.0
    })
    test_endpoint('10. Budget Estimate API', 'GET', '/api/v1/budget/estimate?destination=Tokyo&days=3')
    test_endpoint('11. Smart Packing Checklist API', 'POST', '/api/v1/packing/generate', {
        'destination': 'Goa',
        'days': 3,
        'season': 'Summer',
        'activities': ['Beach', 'Dining']
    })
    test_endpoint('12. Phrasebook Curated Phrases API', 'POST', '/api/v1/phrasebook/phrases', {
        'language': 'Hindi',
        'category': 'Greetings'
    })
    test_endpoint('13. Phrasebook Text Translation API', 'POST', '/api/v1/phrasebook/translate', {
        'text': 'Where is the train station?',
        'source_language': 'English',
        'target_language': 'Spanish'
    })
    test_endpoint('14. Audio Speech Stream API', 'GET', '/api/v1/phrasebook/audio?text=Hello&lang=es')
    test_endpoint('15. AI Chat Planning API', 'POST', '/api/v1/chat/message', {
        'messages': [{'role': 'user', 'content': 'Plan a 3 day trip to Bali'}],
        'destination': 'Bali'
    })

    # Test 16: Structured AI Chat Masterplan Generator API
    test_endpoint('16. AI Chat Masterplan Plan Generator', 'POST', '/api/v1/chat/plan', {
        'destination': 'Vietnam',
        'days': 7,
        'party': 'Couple',
        'budget': 'Balanced'
    })

    # Test 17: Vision Analyze API (Multipart with valid PIL image)
    img = Image.new('RGB', (120, 120), color=(50, 120, 180))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    valid_jpg_bytes = buf.getvalue()

    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body_part1 = (
        f'--{boundary}\r\n'
        'Content-Disposition: form-data; name="mode"\r\n\r\n'
        'landmark\r\n'
        f'--{boundary}\r\n'
        'Content-Disposition: form-data; name="file"; filename="taj_mahal_test.jpg"\r\n'
        'Content-Type: image/jpeg\r\n\r\n'
    ).encode('utf-8')
    body_part2 = f'\r\n--{boundary}--\r\n'.encode('utf-8')
    full_multipart = body_part1 + valid_jpg_bytes + body_part2
    
    test_endpoint(
        '16. Multimodal Vision Analyze API',
        'POST',
        '/api/v1/vision/analyze',
        data=full_multipart,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
        is_json=False,
        is_multipart=True
    )

    print("\n==================================================")
    print("                  TEST RESULTS                    ")
    print("==================================================")
    passed_count = sum(1 for r in results if r[1] == 'PASS')
    failed_count = sum(1 for r in results if r[1] == 'FAIL')
    
    for name, outcome, code, err in results:
        status_sym = "[OK]" if outcome == 'PASS' else "[FAILED]"
        print(f"{status_sym} {name} (HTTP {code})")
        if err:
            print(f"     Details: {err}")
            
    print(f"\nSummary: {passed_count}/{len(results)} endpoints passed ({passed_count/len(results)*100:.1f}%)")
    if failed_count == 0:
        print("ALL ENDPOINTS AND SERVICES ARE 100% OPERATIONAL!")
    else:
        print(f"ATTENTION: {failed_count} endpoint(s) require attention.")

if __name__ == '__main__':
    run_all_tests()
