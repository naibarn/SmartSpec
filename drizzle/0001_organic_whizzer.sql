CREATE TABLE `gallery_items` (
	`id` int AUTO_INCREMENT NOT NULL,
	`type` enum('image','video','website') NOT NULL,
	`title` varchar(255) NOT NULL,
	`description` text,
	`aspectRatio` enum('1:1','9:16','16:9') NOT NULL,
	`fileKey` varchar(512),
	`fileUrl` varchar(1024),
	`thumbnailKey` varchar(512),
	`thumbnailUrl` varchar(1024),
	`duration` varchar(10),
	`demoUrl` varchar(512),
	`tags` json DEFAULT ('[]'),
	`views` int NOT NULL DEFAULT 0,
	`likes` int NOT NULL DEFAULT 0,
	`downloads` int NOT NULL DEFAULT 0,
	`isPublished` boolean NOT NULL DEFAULT true,
	`isFeatured` boolean NOT NULL DEFAULT false,
	`authorId` int,
	`authorName` varchar(255),
	`authorAvatar` varchar(512),
	`sortOrder` int NOT NULL DEFAULT 0,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `gallery_items_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
ALTER TABLE `gallery_items` ADD CONSTRAINT `gallery_items_authorId_users_id_fk` FOREIGN KEY (`authorId`) REFERENCES `users`(`id`) ON DELETE no action ON UPDATE no action;