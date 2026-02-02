"""
Classifier for Spanish Municipalities
Classifies municipalities as Rural or Urban based on population threshold
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import POPULATION_THRESHOLD, LABEL_RURAL, LABEL_URBAN


class MunicipalityClassifier:
    """Classifier for rural vs urban municipalities"""

    def __init__(self, threshold=None):
        """
        Initialize classifier with population threshold

        Args:
            threshold: Population threshold (default from config)
                      Below threshold = Rural
                      Above or equal threshold = Urban
        """
        self.threshold = threshold or POPULATION_THRESHOLD

    def classify(self, population):
        """
        Classify a single municipality based on population

        Args:
            population: Population count (int or None)

        Returns:
            Classification label (str)
        """
        if population is None:
            return LABEL_RURAL  # Default to rural if unknown

        if population < self.threshold:
            return LABEL_RURAL
        else:
            return LABEL_URBAN

    def classify_all(self, municipalities):
        """
        Classify all municipalities and add classification field

        Args:
            municipalities: List of municipality dictionaries

        Returns:
            List of municipalities with 'classification' field added
        """
        classified = []

        for m in municipalities:
            m_copy = m.copy()
            m_copy['classification'] = self.classify(m.get('population'))
            classified.append(m_copy)

        return classified

    def get_statistics(self, municipalities):
        """
        Get classification statistics

        Args:
            municipalities: List of classified municipalities

        Returns:
            Dictionary with statistics
        """
        total = len(municipalities)
        rural = sum(1 for m in municipalities if m.get('classification') == LABEL_RURAL)
        urban = sum(1 for m in municipalities if m.get('classification') == LABEL_URBAN)

        return {
            'total': total,
            'rural': rural,
            'urban': urban,
            'rural_percentage': round(rural / total * 100, 2) if total > 0 else 0,
            'urban_percentage': round(urban / total * 100, 2) if total > 0 else 0
        }


def main():
    """Test the classifier"""
    classifier = MunicipalityClassifier()

    # Test data
    test_municipalities = [
        {'name': 'Madrid', 'population': 3223334},
        {'name': 'Barcelona', 'population': 1620343},
        {'name': 'Villanueva', 'population': 2500},
        {'name': 'Pueblecito', 'population': 150},
        {'name': 'Unknown', 'population': None}
    ]

    classified = classifier.classify_all(test_municipalities)

    print("Classification Results:")
    print("-" * 50)
    for m in classified:
        print(f"{m['name']}: {m['population']} -> {m['classification']}")

    stats = classifier.get_statistics(classified)
    print("\nStatistics:")
    print(f"  Total: {stats['total']}")
    print(f"  Rural: {stats['rural']} ({stats['rural_percentage']}%)")
    print(f"  Urban: {stats['urban']} ({stats['urban_percentage']}%)")


if __name__ == "__main__":
    main()
