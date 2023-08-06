from .base import ReboticsBaseProvider, remote_service


class HawkeyeProvider(ReboticsBaseProvider):

    @remote_service('/api/camera/heartbeats/')
    def save_camera_heartbeat(self, shelf_camera, battery_status, free_storage, used_storage):
        return self.session.post(json={
            "shelf_camera": shelf_camera,
            "battery_status": battery_status,
            "free_storage": free_storage,
            "used_storage": used_storage
        })

    @remote_service('/api/camera/camera-actions/')
    def save_camera_action(self, action_type, status_type, payload, shelf_camera):
        return self.session.post(json={
            "action_type": action_type,
            "status_type": status_type,
            "payload": payload,
            "shelf_camera": shelf_camera
        })

    @remote_service('/api/camera/camera-actions/')
    def get_camera_actions(self):
        return self.session.get()

    @remote_service('/api/camera/retailer/')
    def save_retailer(self, codename, token):
        return self.session.post(json={
            "retailer": codename,
            "token": token
        })

    @remote_service('/api/camera/fixtures/')
    def save_fixture(self, retailer, store_id, aisle, section):
        return self.session.post(
            json={
                "store_id": store_id,
                "aisle": aisle,
                "section": section,
                "retailer": retailer
            }
        )

    @remote_service('/api/camera/fixtures/{id}')
    def delete_fixture(self, pk):
        return self.session.delete(id=pk)

    @remote_service('/api/camera/fixtures/')
    def get_fixtures(self):
        return self.session.get()

    @remote_service('/api/camera/shelf-cameras/')
    def create_shelf_camera(self, camera_id, added_by, fixture=None):
        data = {
            "camera_id": camera_id,
            "added_by": added_by,
        }
        if fixture is not None:
            data["fixture"] = fixture
        return self.session.post(json=data)

    @remote_service('/api/camera/shelf-cameras/')
    def get_shelf_cameras(self):
        return self.session.get()

    @remote_service('/api/fetcher/{camera_id}/')
    def save_capture(self, camera, file_key, bucket_name):
        return self.session.post(
            camera_id=camera,
            json={
                "file_key": file_key,
                "bucket_name": bucket_name
            })

    @remote_service('/api/camera/mac-address/search/')
    def search_camera_by_mac(self, mac_address):
        assert ":" in mac_address, "Mac address should be separated by : (colon)"
        return self.session.post(json={
            'mac_address': mac_address
        })

    @remote_service('/api/camera/mac-address/')
    def create_mac_address_link(self, mac_address, vendor_secret, rebotics_secret):
        assert ":" in mac_address, "Mac address should be separated by : (colon)"
        return self.session.post(json={
            'mac_address': mac_address,
            'vendor_secret': vendor_secret,
            'rebotics_secret': rebotics_secret,
        })

    @remote_service('/api/camera/mac-address/{id}/')
    def update_mac_address_link(self, id_, mac_address, vendor_secret, rebotics_secret):
        assert ":" in mac_address, "Mac address should be separated by : (colon)"
        assert isinstance(id_, int), "Link ID should be integer, use search by mac-address to determine Link ID"
        return self.session.patch(id=id_, json={
            'mac_address': mac_address,
            'vendor_secret': vendor_secret,
            'rebotics_secret': rebotics_secret,
        })

    @remote_service('/api/camera/mac-address/{id}/', raw=True)
    def delete_mac_address_link(self, id_):
        response = self.session.delete(id=id_)
        response.raise_for_status()
