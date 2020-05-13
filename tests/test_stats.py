from rest_framework import status
from rest_framework.reverse import reverse


def test_countries_list(db, client, live_statistics):
    response = client.get(reverse("stats:country-list"),
                          content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert len(data) == 5


def test_countries_get(db, client, live_statistics):
    country = live_statistics[0]['country']
    response = client.get(reverse("stats:country-detail",
                                  kwargs={"pk": country.pk}),
                          content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data["name"] == country.name
    assert len(data['statistics'][0]) == 9
