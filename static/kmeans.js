// modified from https://github.com/harthur/clusterfck/blob/master/lib/kmeans.js

/* centroid must be a point
   distance must compare two points
*/

function closestCentroid(point, centroids, distance) {
   var min = Infinity,
       index = 0;
   for (var i = 0; i < centroids.length; i++) {
      var dist = distance(point, centroids[i]);
      if (dist < min) {
         min = dist;
         index = i;
      }
   }
   return index;
}

function kmeans(points, k, distance, centroids, updateCentroidToAverageOfPoints) {
    // updateCentroidToAverageOfPoints is a function taking in centroid and array of points,
    //  it should mutate the centroid
    //  and return a bool which says whether or not the centroid moved.
   k = k || Math.max(2, Math.ceil(Math.sqrt(points.length / 2)));

   var assignment = new Array(points.length);
   var clusters = new Array(k);

   var iterations = 0;
   var movement = true;
   while (movement) {
      // update point-to-centroid assignments
      for (var i = 0; i < points.length; i++) {
         assignment[i] = closestCentroid(points[i], centroids, distance);
      }

      // update location of each centroid
      movement = false;
      for (var j = 0; j < k; j++) {
         var assigned = [];
         for (var i = 0; i < assignment.length; i++) {
            if (assignment[i] == j) {
               assigned.push(points[i]);
            }
         }

         if (!assigned.length) {
            continue;
         }
         var centroid = centroids[j];

         movement = updateCentroidToAverageOfPoints(centroid, assigned);

         clusters[j] = assigned;
      }
   }
   return clusters;
}
