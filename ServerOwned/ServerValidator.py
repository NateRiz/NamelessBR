class ServerValidator:
    @staticmethod
    def validate_change_rooms( src, dest) -> bool:
        """
        Validate that the source room is one away from the destination. Not diagonally either.
        :param src: source coordinate
        :param dest: destination coordinate
        :return: Whether the request is valid
        """
        src_y, src_x = src
        dest_y, dest_x = dest

        if src_y == dest_y:
            if abs(src_x - dest_x) == 1:
                return True
        elif src_x == dest_x:
            if abs(src_y - dest_y) == 1:
                return True

        return False
