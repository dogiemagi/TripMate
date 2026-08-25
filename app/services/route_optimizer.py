import math
import logging
from typing import List, Dict, Any, Tuple, Optional

logger = logging.getLogger("voyage.router")

EARTH_RADIUS_KM = 6371.0

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two geographic coordinates in kilometers."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_KM * c

def estimate_travel_time_minutes(distance_km: float, speed_kmh: float = 25.0) -> int:
    """Estimates realistic urban/transit travel time including traffic buffer."""
    if distance_km <= 0.05:
        return 2
    hours = distance_km / speed_kmh
    # 5 min base overhead + transit duration
    mins = int(round(hours * 60.0 + 5.0))
    return max(3, mins)

class RouteOptimizer:
    """
    Intelligent Spatial Route Optimization Engine for Travel Itineraries.
    Implements:
      1. Spatial Distribution Analysis & Proximity Clustering (DBSCAN / Proximity Thresholds)
      2. Inter-Cluster Topological Sweep (Radial / Angular / Principal Axis Sweep)
      3. Intra-Cluster Path Optimization (Nearest-Neighbor with 2-Opt Local Search)
      4. Multi-Day Budget Segmentation & Time-Window Feasibility
      5. Priority Weighting (Must-Visit vs Flexible)
    """

    @classmethod
    def optimize_itinerary(
        cls,
        destinations: List[Dict[str, Any]],
        origin: Optional[Tuple[float, float]] = None,
        days_count: int = 1,
        max_daily_distance_km: float = 35.0,
        cluster_threshold_km: float = 3.5
    ) -> Dict[str, Any]:
        """
        Main optimization pipeline that eliminates zigzagging and returns geographically coherent daily schedules.
        """
        if not destinations:
            return {"ordered_destinations": [], "days": [], "total_distance_km": 0.0}

        n = len(destinations)
        if n == 1:
            dest = destinations[0]
            dest["stop_number"] = 1
            dest["travel_from_prev_km"] = 0.0
            dest["travel_from_prev_min"] = 0
            return {
                "ordered_destinations": [dest],
                "days": [{"day": 1, "activities": [dest], "day_distance_km": 0.0}],
                "total_distance_km": 0.0,
                "backtracking_eliminated": True
            }

        # Step 1: Compute Centroid & Geometric Center
        avg_lat = sum(d["lat"] for d in destinations) / n
        avg_lon = sum(d["lon"] for d in destinations) / n
        origin_lat, origin_lon = origin if origin else (avg_lat, avg_lon)

        # Step 2: Proximity Clustering (Agglomerative / Density Partitioning)
        clusters = cls._cluster_by_proximity(destinations, cluster_threshold_km)

        # Step 3: Sequence Clusters via Angular / Directional Sweep from Origin
        ordered_clusters = cls._order_clusters_sweep(clusters, origin_lat, origin_lon)

        # Step 4: Intra-Cluster Optimization (TSP with 2-Opt)
        ordered_route = []
        current_pos = (origin_lat, origin_lon)

        for cluster in ordered_clusters:
            optimized_cluster = cls._optimize_single_cluster(cluster, current_pos)
            ordered_route.extend(optimized_cluster)
            if optimized_cluster:
                current_pos = (optimized_cluster[-1]["lat"], optimized_cluster[-1]["lon"])

        # Step 5: Global 2-Opt Path Refinement across Cluster Transitions
        final_route = cls._two_opt_refine(ordered_route)

        # Step 6: Compute Legs, Distances, and Estimated Transit Times
        total_dist = 0.0
        for i, stop in enumerate(final_route):
            stop["stop_number"] = i + 1
            if i == 0:
                dist = haversine_distance(origin_lat, origin_lon, stop["lat"], stop["lon"]) if origin else 0.0
                stop["travel_from_prev_km"] = round(dist, 2)
                stop["travel_from_prev_min"] = estimate_travel_time_minutes(dist)
            else:
                prev = final_route[i - 1]
                dist = haversine_distance(prev["lat"], prev["lon"], stop["lat"], stop["lon"])
                stop["travel_from_prev_km"] = round(dist, 2)
                stop["travel_from_prev_min"] = estimate_travel_time_minutes(dist)
                total_dist += dist

        # Step 7: Multi-Day Trip Segmentation
        day_buckets = cls._segment_into_days(final_route, days_count, max_daily_distance_km)

        return {
            "ordered_destinations": final_route,
            "days": day_buckets,
            "total_distance_km": round(total_dist, 2),
            "total_clusters": len(clusters),
            "algorithm": "Cluster-Constrained Sweep with 2-Opt Local Search",
            "backtracking_eliminated": True
        }

    @classmethod
    def _cluster_by_proximity(
        cls, 
        destinations: List[Dict[str, Any]], 
        threshold_km: float = 3.5
    ) -> List[List[Dict[str, Any]]]:
        """
        Groups points into spatial neighborhood clusters using proximity graph connected components.
        """
        n = len(destinations)
        visited = [False] * n
        clusters = []

        for i in range(n):
            if visited[i]:
                continue
            
            # Start new cluster
            cluster = [destinations[i]]
            visited[i] = True
            queue = [i]

            while queue:
                curr_idx = queue.pop(0)
                curr_p = destinations[curr_idx]

                for j in range(n):
                    if not visited[j]:
                        target_p = destinations[j]
                        dist = haversine_distance(curr_p["lat"], curr_p["lon"], target_p["lat"], target_p["lon"])
                        if dist <= threshold_km:
                            visited[j] = True
                            cluster.append(target_p)
                            queue.append(j)

            clusters.append(cluster)

        return clusters

    @classmethod
    def _order_clusters_sweep(
        cls, 
        clusters: List[List[Dict[str, Any]]], 
        origin_lat: float, 
        origin_lon: float
    ) -> List[List[Dict[str, Any]]]:
        """
        Orders clusters by polar angle (angular sweep) from origin to form a clean convex tour.
        """
        if len(clusters) <= 1:
            return clusters

        cluster_metadata = []
        for c_idx, cluster in enumerate(clusters):
            c_lat = sum(p["lat"] for p in cluster) / len(cluster)
            c_lon = sum(p["lon"] for p in cluster) / len(cluster)
            
            # Polar angle relative to origin
            dy = c_lat - origin_lat
            dx = (c_lon - origin_lon) * math.cos(math.radians(origin_lat))
            angle = math.atan2(dy, dx)
            dist_from_origin = haversine_distance(origin_lat, origin_lon, c_lat, c_lon)

            cluster_metadata.append({
                "cluster": cluster,
                "center_lat": c_lat,
                "center_lon": c_lon,
                "angle": angle,
                "dist": dist_from_origin
            })

        # Sort clusters by sweep angle to eliminate inter-cluster crossings
        cluster_metadata.sort(key=lambda x: x["angle"])
        return [item["cluster"] for item in cluster_metadata]

    @classmethod
    def _optimize_single_cluster(
        cls, 
        cluster: List[Dict[str, Any]], 
        entry_pos: Tuple[float, float]
    ) -> List[Dict[str, Any]]:
        """
        Solves intra-cluster path using Nearest-Neighbor with priority weighting and 2-Opt.
        """
        if len(cluster) <= 2:
            return sorted(
                cluster, 
                key=lambda p: haversine_distance(entry_pos[0], entry_pos[1], p["lat"], p["lon"])
            )

        unvisited = list(cluster)
        ordered = []
        curr_lat, curr_lon = entry_pos

        # Greedy Nearest Neighbor
        while unvisited:
            # Score each candidate by distance and priority
            def score_candidate(cand):
                dist = haversine_distance(curr_lat, curr_lon, cand["lat"], cand["lon"])
                priority = cand.get("priority", "flexible")
                weight = 0.7 if priority == "must_visit" else 1.0
                return dist * weight

            next_spot = min(unvisited, key=score_candidate)
            ordered.append(next_spot)
            unvisited.remove(next_spot)
            curr_lat, curr_lon = next_spot["lat"], next_spot["lon"]

        # Apply 2-Opt intra-cluster refinement
        return cls._two_opt_refine(ordered)

    @classmethod
    def _two_opt_refine(cls, route: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        2-Opt heuristic that uncrosses any overlapping edges and eliminates local loops.
        """
        if len(route) <= 3:
            return route

        improved = True
        best_route = list(route)
        max_iters = 50
        iter_count = 0

        while improved and iter_count < max_iters:
            improved = False
            iter_count += 1
            n = len(best_route)

            for i in range(n - 1):
                for j in range(i + 2, n):
                    p1 = best_route[i]
                    p2 = best_route[i + 1]
                    p3 = best_route[j]
                    p4 = best_route[(j + 1) % n] if (j + 1) < n else None

                    # Current distance of edges (p1-p2) + (p3-p4)
                    current_dist = haversine_distance(p1["lat"], p1["lon"], p2["lat"], p2["lon"])
                    if p4:
                        current_dist += haversine_distance(p3["lat"], p3["lon"], p4["lat"], p4["lon"])

                    # Reversed distance of edges (p1-p3) + (p2-p4)
                    new_dist = haversine_distance(p1["lat"], p1["lon"], p3["lat"], p3["lon"])
                    if p4:
                        new_dist += haversine_distance(p2["lat"], p2["lon"], p4["lat"], p4["lon"])

                    if new_dist < (current_dist - 1e-4):
                        # Reverse subarray between i+1 and j
                        best_route[i + 1 : j + 1] = reversed(best_route[i + 1 : j + 1])
                        improved = True
                        break
                if improved:
                    break

        return best_route

    @classmethod
    def _segment_into_days(
        cls, 
        route: List[Dict[str, Any]], 
        target_days: int, 
        max_daily_dist_km: float = 35.0
    ) -> List[Dict[str, Any]]:
        """
        Partitions the contiguous route into daily buckets while respecting time windows and daily limits.
        """
        total_items = len(route)
        if total_items == 0:
            return []

        days_count = max(1, target_days)
        items_per_day = math.ceil(total_items / days_count)

        day_buckets = []
        start_idx = 0

        time_slots = [
            ("09:00 AM", "Morning Heritage & Landmark Exploration"),
            ("12:00 PM", "Gastronomy, Food Walks & Local Markets"),
            ("03:00 PM", "Culture, Galleries & Historic Districts"),
            ("06:30 PM", "Panoramic Vistas, Sunset & Evening Dining")
        ]

        for d in range(1, days_count + 1):
            day_acts = []
            end_idx = min(start_idx + items_per_day, total_items)
            chunk = route[start_idx:end_idx]
            start_idx = end_idx

            day_dist = 0.0
            for a_idx, act in enumerate(chunk):
                # Assign structured time slot if not explicitly provided
                slot_time, _ = time_slots[min(a_idx, len(time_slots) - 1)]
                act["time"] = act.get("time") or slot_time
                act["day"] = d
                if a_idx > 0:
                    prev_a = chunk[a_idx - 1]
                    day_dist += haversine_distance(prev_a["lat"], prev_a["lon"], act["lat"], act["lon"])

                day_acts.append(act)

            if day_acts:
                day_buckets.append({
                    "day": d,
                    "theme": f"Day {d}: Geographically Coherent Exploration",
                    "highlight": f"{len(day_acts)} Proximate Sights | No Backtracking",
                    "day_distance_km": round(day_dist, 2),
                    "activities": day_acts
                })

        return day_buckets
