from rest_framework.decorators import api_view
from rest_framework.response import Response

from .decorators import decorator_redis_connection
from .utils.constants import LEADER_BOARD


@api_view(['POST'])
@decorator_redis_connection
def add_player_info(request):
    redis_connection = request.redis_connection
    id_ = request.data.get('id')
    score = request.data.get('score')

    if id_ is None or score is None:
        return Response({'status': False, 'message': 'Check inputs'})

    added = redis_connection.zadd(LEADER_BOARD, str(id_), score)

    return Response({
            'status': added,
            'message': 'success'
        })


@api_view(['GET'])
@decorator_redis_connection
def get_player_info(request):
    redis_connection = request.redis_connection
    id_ = request.query_params.get('id')

    if id_ is None:
        return Response({'status': False, 'message': 'Check inputs'})

    score = redis_connection.zscore(LEADER_BOARD, str(id_))

    if not score:
        return Response({
            'status': False,
            'message': 'player id does not exist'
        })

    response_data = {
        'score': score,
        'rank': 1 + redis_connection.zrevrank(
            LEADER_BOARD, redis_connection.zrevrangebyscore(LEADER_BOARD, score, score, start=0, num=1)[0]
        )
    }

    return Response(response_data)


@api_view(['PATCH'])
@decorator_redis_connection
def update_player_info(request):
    redis_connection = request.redis_connection
    id_ = request.data.get('id')
    score = request.data.get('score')

    if id_ is None or score is None:
        return Response({'status': False, 'message': 'Check inputs'})

    redis_connection.zadd('leader_board', str(id_), score)

    return Response({
        'status': True,
        'message': 'success'
    })
