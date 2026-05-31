# Import all models here so Alembic autogenerate can discover them.
from src.modules.users.models.user import UserModel  # noqa: F401
from src.modules.content.models.category import CategoryModel  # noqa: F401
from src.modules.content.models.topic import TopicModel  # noqa: F401
from src.modules.content.models.subtopic import SubtopicModel  # noqa: F401
from src.modules.content.models.exercise import ExerciseModel  # noqa: F401
from src.modules.content.models.exercise_mc import ExerciseMCModel  # noqa: F401
from src.modules.content.models.exercise_tf import ExerciseTFModel  # noqa: F401
from src.modules.content.models.exercise_image import ExerciseImageModel  # noqa: F401
from src.modules.content.models.exercise_match import ExerciseMatchPairModel  # noqa: F401
from src.modules.content.models.exercise_map import ExerciseMapConfigModel, ExerciseMapHotspotModel  # noqa: F401
from src.modules.content.models.exercise_chrono import ExerciseChronoItemModel  # noqa: F401
from src.modules.content.models.exercise_estimation import ExerciseEstimationModel  # noqa: F401
from src.modules.sessions.models.session import SessionModel  # noqa: F401
from src.modules.answers.models.answer import AnswerModel  # noqa: F401
from src.modules.answers.models.answer_mc import AnswerMCModel  # noqa: F401
from src.modules.answers.models.answer_tf import AnswerTFModel  # noqa: F401
from src.modules.answers.models.answer_image import AnswerImageModel  # noqa: F401
from src.modules.answers.models.answer_match import AnswerMatchModel  # noqa: F401
from src.modules.answers.models.answer_map import AnswerMapModel  # noqa: F401
from src.modules.answers.models.answer_chrono import AnswerChronoModel  # noqa: F401
from src.modules.answers.models.answer_estimation import AnswerEstimationModel  # noqa: F401
