// Define the class macro for this thing.
#ifndef MANUKA_CHUNK_H
#define MANUKA_CHUNK_H

// Godot stuff that we're using.
#include <godot_cpp/classes/control.hpp>
#include <godot_cpp/classes/global_constants.hpp>
#include <godot_cpp/core/binder_common.hpp>
#include <godot_cpp/classes/static_body3d.hpp>
#include <godot_cpp/classes/mesh_instance3d.hpp>
#include <godot_cpp/classes/array_mesh.hpp>

using namespace godot;

namespace manuka {
class Chunk : public MeshInstance3D{
	GDCLASS(Chunk, MeshInstance3D)

	godot::PackedVector3Array vertices;
	godot::PackedVector2Array uvs;
	godot::Array surface_arrays;

	godot::PackedInt32Array triangles;

	godot::ArrayMesh array_mesh;
	Vector2 custom_position;

protected:
	static void _bind_methods();
public:
	Chunk();
	~Chunk();

	// Declare functions here.
	void print_something(const String& thing);
	void add_voxel_data_to_chunk(const godot::Vector3& position);
	void populate_voxel_map();
	void create_mesh_data();
	bool check_voxel(const godot::Vector3& position);

	Ref<Mesh> create_mesh(); // Keep in mind: Godot likes Refs when returning stuff.
};

} // Namespace manuka.

#endif // MANUKA_CHUNK_H